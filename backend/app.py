import os
import re
import traceback
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from utils.ai_simplifier import AISimplifier
from utils.database import save_document_history, get_user_history
from utils.cloud_storage import upload_document_to_cloud

app = Flask(__name__)

# ==========================================================
# 🌐 UNIVERSAL CORS CONFIG (Final Production-Ready)
# ==========================================================

# Get production frontend URL from Render env
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://aisimplifierfrontend.netlify.app')

# Enable wildcard CORS safely for Netlify + localhost
CORS(
    app,
    resources={r"/api/*": {"origins": [
        FRONTEND_URL,
        "https://aisimplifierfrontend.netlify.app",
        re.compile(r"^https://[a-zA-Z0-9-]+--aisimplifierfrontend\.netlify\.app$"),  # all preview builds
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    supports_credentials=False,
)

# ==========================================================
# 🤖 Initialize AI Simplifier
# ==========================================================
try:
    ai_simplifier = AISimplifier()
    print("✅ Gemini Simplifier initialized successfully.")
except Exception as e:
    print(f"FATAL: Could not initialize AISimplifier: {e}")
    ai_simplifier = None

# ==========================================================
# 🧠 API ROUTES
# ==========================================================
@app.route('/')
def home():
    return jsonify({"message": "Legal Document Simplifier API", "status": "running"})

@app.route('/api/health', methods=['GET'])
def health_check():
    is_ready = ai_simplifier is not None and getattr(ai_simplifier, "available", False)
    return jsonify({
        "status": "ok" if is_ready else "error",
        "message": "Service is running." if is_ready else "AI Simplifier not available.",
        "simplifier_ready": is_ready
    }), 200 if is_ready else 503

@app.route('/api/simplify', methods=['POST'])
def simplify_document_route():
    if not ai_simplifier or not getattr(ai_simplifier, "available", False):
        return jsonify({"success": False, "error": "AI Simplifier not available"}), 503

    document_text = ""

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        try:
            document_text = file.read().decode('utf-8')
        except Exception as e:
            return jsonify({"success": False, "error": f"Error reading file: {e}"}), 400
    elif request.is_json:
        data = request.get_json()
        document_text = data.get('text', '')
    else:
        return jsonify({"success": False, "error": "Provide file or JSON with 'text'"}), 400

    if not document_text.strip():
        return jsonify({"success": False, "error": "Document text is empty"}), 400

    try:
        simplified_text = ai_simplifier.simplify_text(document_text)
        return jsonify({"success": True, "simplified_text": simplified_text})
    except Exception:
        traceback.print_exc()
        return jsonify({"success": False, "error": "Unexpected error during simplification"}), 500

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = os.getenv('FRONTEND_URL', 'https://aisimplifierfrontend.netlify.app')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

# ==========================================================
# 🚀 Render Production Entrypoint
# ==========================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
