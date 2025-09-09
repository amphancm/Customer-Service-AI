from flask import Flask, send_from_directory, jsonify , request, abort
from routes import register_routes
from config import Config
from flask_cors import CORS
import logging, os
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
from controllers.auth_controller import blacklist
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import mammoth , requests
from io import BytesIO
from db import Connection
import uuid
from flask_cors import CORS








logger = logging.getLogger(__name__)

MILVUS_HOST = os.environ.get('MILVUS_HOST', 'milvus')
MILVUS_PORT = os.environ.get('MILVUS_PORT', '19530')
VLLM_HOST = os.environ.get('VLLM_HOST', '172.17.0.1:8000')

app = Flask(__name__)
# Enable CORS with full access for development
CORS(app, expose_headers=["Content-Disposition"])
app.config.from_object(Config)
register_routes(app)
mongo=Connection('otg_db')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

def create_default_user():
    default_username = "admin"
    default_email = "admin@admin.com"
    default_password = "admin"

    user = mongo.accounts.count_documents({"username": default_username})
    
    if not user:
        encrypted_password = generate_password_hash(default_password)

        mongo.accounts.insert_one({
            "username": default_username,
            "email": default_email,
            "role": "administrator",
            "password": encrypted_password,
        })
        logger.info("Default user created.")
    else:
        logger.info("Default user already exists.")

    if mongo.systemPrompt.count_documents({}) == 0:
        mongo.systemPrompt.insert_one({
            "content":"",
            "temperature":"",
        })
        logger.info("Default system Prompt created.")
    else:
        logger.info("Default system Prompt already exists.")

    if mongo.setting.count_documents({}) == 0:
        mongo.setting.insert_one({
            "time_activate": True,
            "line_activate": False,
            "fb_activate": False,
            "product_activate": False,
            "feedback_activate": False,
            "greeting_activate": False,
            "line_key": "",
            "line_secret": "",
            "facebook_token": "",
            "facebook_verify_password": "",
            "greeting_prompt": "",
        })
        logger.info("Default system setting created.")
    else:
        logger.info("Default system setting already exists.")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




ALLOWED_EXTENSIONS = {'txt', 'docx'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload a .txt, .docx file or Google Doc (by URL).
    Returns file content for use in a text box.
    """
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            original_filename = file.filename
            ext = original_filename.rsplit('.', 1)[1].lower()
            content = ""

            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

            if ext == "txt":
                try:
                    content = file.read().decode('utf-8')
                except UnicodeDecodeError:
                    # Fallback for different encodings if UTF-8 fails
                    content = file.read().decode('latin-1') # Or 'tis-620' for specific Thai context if UTF-8 isn't used
            elif ext == "docx":
                with BytesIO(file.read()) as docx_io:
                    result = mammoth.extract_raw_text(docx_io)
                    content = result.value  # The extracted text
            else:
                return jsonify({'error': 'Unsupported file type'}), 400

            # Save file if needed
            file.seek(0) # Reset file pointer after reading content
            file.save(filepath)

            # Return original filename for display if desired, even if saved with unique name
            return jsonify({'message': 'File uploaded', 'filename': original_filename, 'saved_as': unique_filename, 'content': content}), 201
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    elif request.is_json:
        data = request.get_json()
        gdoc_url = data.get('gdoc_url')
        if gdoc_url:
            if "/document/d/" in gdoc_url:
                doc_id = gdoc_url.split("/d/")[1].split("/")[0]
                export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
                resp = requests.get(export_url)
                if resp.status_code == 200:
                    content = resp.text
                    # Google Docs doesn't provide a filename, so we generate one.
                    # This will not be a problem with Thai characters as it's generated.
                    filename = f"gdoc_{doc_id}.txt"
                    # Optionally, save file if needed
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return jsonify({'message': 'Google Doc downloaded', 'filename': filename, 'content': content}), 201
                else:
                    return jsonify({'error': 'Failed to fetch Google Doc'}), 400
            else:
                return jsonify({'error': 'Invalid Google Doc URL'}), 400

    return jsonify({'error': 'No file or Google Doc URL provided'}), 400



@app.route('/model_list', methods=['GET'])
def model_list():
    return jsonify({
        "domain_name": [
            {"label": "openrounter", "value": "https://openrouter.ai/api/v1"},
            {"label": "opentogether", "value": "https://api.together.xyz/v1"},
            # {"label": "ollama", "value": True}
        ]
    })



create_default_user()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)




    