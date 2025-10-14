import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.ai_simplifier import AISimplifier
from utils.database import save_document_history, get_user_history
from utils.cloud_storage import upload_document_to_cloud
import traceback

app = Flask(__name__)

# Use FRONTEND_URL from environment variable or fallback to local
frontend_url = os.getenv('FRONTEND_URL', 'https://aisimplifier.netlify.app')
CORS(app, resources={r"/api/*": {"origins": [frontend_url, "http://localhost:5001", "http://localhost:3000"]}})

# Initialize AISimplifier
try:
    ai_simplifier = AISimplifier()
except Exception as e:
    print(f"FATAL: Could not initialize AISimplifier: {e}")
    ai_simplifier = None

@app.route('/')
def home():
    return jsonify({"message": "Legal Document Simplifier API", "status": "running"})

@app.route('/api/health', methods=['GET'])
def health_check():
    is_ready = ai_simplifier is not None and ai_simplifier.available
    return jsonify({
        "status": "ok" if is_ready else "error",
        "message": "Service is running." if is_ready else "AI Simplifier is not available.",
        "simplifier_ready": is_ready
    }), 200 if is_ready else 503

@app.route('/api/simplify', methods=['POST'])
def simplify_document_route():
    if not ai_simplifier or not ai_simplifier.available:
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

# -------------------------------
# Render Deployment Configuration
# -------------------------------
if __name__ == '__main__':
    # Use PORT from environment variable (Render provides it)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
