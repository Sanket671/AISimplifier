import os
import re
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import project utilities
from utils.ai_simplifier import AISimplifier
from utils.database import save_document_history, get_user_history, get_mongodb_client
from utils.cloud_storage import upload_document_to_cloud

# ==========================================================
# ⚙️ Flask App Initialization
# ==========================================================
app = Flask(__name__)

# ==========================================================
# 🌐 UNIVERSAL CORS CONFIG (Production-Ready)
# ==========================================================
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://aisimplifierfrontend.netlify.app')

CORS(app, origins="*", supports_credentials=True)

# ==========================================================
# 🤖 Initialize AI Simplifier
# ==========================================================
try:
    ai_simplifier = AISimplifier()
    print("✅ Gemini Simplifier initialized successfully.")
except Exception as e:
    print(f"❌ FATAL: Could not initialize AISimplifier: {e}")
    ai_simplifier = None

# ==========================================================
# 🧩 Initialize MongoDB Connection (on startup)
# ==========================================================
try:
    client = get_mongodb_client()
    if client:
        print("✅ MongoDB connection initialized successfully.")
        client.close()
    else:
        print("❌ MongoDB client could not be created.")
except Exception as e:
    print(f"⚠️ Error initializing MongoDB: {e}")

# ==========================================================
# 🧠 API ROUTES
# ==========================================================

@app.route('/')
def home():
    """Default route for API health."""
    return jsonify({
        "message": "Legal Document Simplifier API",
        "status": "running"
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check route."""
    is_ready = ai_simplifier is not None and getattr(ai_simplifier, "available", False)
    return jsonify({
        "status": "ok" if is_ready else "error",
        "message": "Service is running." if is_ready else "AI Simplifier not available.",
        "simplifier_ready": is_ready
    }), 200 if is_ready else 503


# ==========================================================
# ✨ Simplify Route
# ==========================================================
@app.route('/api/simplify', methods=['POST'])
def simplify_document_route():
    print("\n========================")
    print("📥 /api/simplify CALLED")
    print("========================")
    print("Headers:", dict(request.headers))
    print("request.files.keys():", list(request.files.keys()))
    print("request.form.keys():", list(request.form.keys()))

    if not ai_simplifier or not getattr(ai_simplifier, "available", False):
        print("❌ AI Simplifier not ready")
        return jsonify({"success": False, "error": "AI Simplifier not available"}), 503

    document_text = ""
    filename = None

    # 🧩 File upload case
    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        print(f"📄 File received: {filename}")
        try:
            file_content = file.read()
            document_text = file_content.decode('utf-8', errors='ignore')
            print(f"✅ File decoded successfully ({len(document_text)} characters)")
        except Exception as e:
            print(f"❌ File read error: {e}")
            return jsonify({"success": False, "error": f"Error reading file: {e}"}), 400

    # 🧩 JSON case
    elif request.is_json:
        data = request.get_json()
        document_text = data.get('text', '')
        print(f"📦 JSON text length: {len(document_text)}")

    else:
        print("⚠️ No file or JSON data received")
        return jsonify({"success": False, "error": "Provide file or JSON with 'text'"}), 400

    # 🧩 Validate text
    if not document_text.strip():
        print("⚠️ Document text empty!")
        return jsonify({"success": False, "error": "Document text is empty"}), 400

    # 🧠 Simplify
    try:
        simplified_text = ai_simplifier.simplify_text(document_text)
        print(f"✅ Simplified text generated ({len(simplified_text)} chars)")
    except Exception as e:
        print(f"❌ Simplification failed: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Error during simplification: {str(e)}"}), 500

    # 💾 Save to MongoDB
    try:
        user_session = request.remote_addr or "unknown_user"
        inserted_id = save_document_history(user_session, document_text, simplified_text, filename)
        print(f"✅ MongoDB insert success → ID: {inserted_id}")
    except Exception as e:
        print(f"❌ MongoDB insert failed: {e}")

    # 🎯 Return to frontend
    return jsonify({
        "success": True,
        "simplified_text": simplified_text
    })

# ==========================================================
# 🕒 Fetch User History
# ==========================================================
@app.route('/api/history', methods=['GET'])
def get_user_history_route():
    """Fetch recent simplification history for a user."""
    user_session = request.remote_addr or "unknown_user"
    history = get_user_history(user_session)
    return jsonify({
        "success": True,
        "history": history
    })


# ==========================================================
# 🧪 Test MongoDB Connection + Insert (Debug Route)
# ==========================================================
@app.route('/api/test-db', methods=['GET'])
def test_db_route():
    """Insert a test document and verify MongoDB is working."""
    try:
        client = get_mongodb_client()
        db = client["legal_documents"]
        collection = db["history"]

        test_doc = {
            "user_session": "test_api_route",
            "original_text": "This is a test insertion via /api/test-db",
            "simplified_text": "This is a simplified test.",
            "timestamp": "2025-11-12",
            "status": "test_success"
        }

        result = collection.insert_one(test_doc)
        client.close()

        return jsonify({
            "success": True,
            "message": "✅ Test document inserted successfully.",
            "inserted_id": str(result.inserted_id)
        }), 200

    except Exception as e:
        print(f"❌ /api/test-db failed: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================================
# 🧱 CORS Headers After Response
# ==========================================================
@app.after_request
def add_cors_headers(response):
    allowed_origins = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "https://aisimplifierfrontend.netlify.app",
        "https://aisimplifier.onrender.com",
    ]

    origin = request.headers.get("Origin")
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.route('/api/debug-upload', methods=['POST'])
def debug_upload():
    print("\n============================")
    print("📥 /api/debug-upload CALLED")
    print("============================")
    print("Headers:", dict(request.headers))
    print("request.files.keys():", list(request.files.keys()))
    print("request.form.keys():", list(request.form.keys()))
    print("============================")

    if 'file' not in request.files:
        return jsonify({"success": False, "msg": "No file detected"}), 400

    file = request.files['file']
    name = file.filename
    content = file.read().decode('utf-8')
    print(f"📄 File received: {name} ({len(content)} characters)")
    return jsonify({"success": True, "msg": f"File {name} received", "length": len(content)})



# ==========================================================
# 🚀 Application Entrypoint
# ==========================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
