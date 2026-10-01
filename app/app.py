import os
import requests
import base64
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def safe_json_parse(s):
    import json
    try:
        return json.loads(s)
    except Exception:
        # Try to fix common JSON issues
        s = s.replace("'", '"')  # single to double quotes
        s = re.sub(r',\s*}', '}', s)  # trailing commas in objects
        s = re.sub(r',\s*]', ']', s)  # trailing commas in arrays
        try:
            return json.loads(s)
        except Exception:
            return s  # fallback: return as string

def extract_receipt_info(image_path):
    # Base64 encode the image
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the prompt for the vision model
    prompt = """
    Extrahieren Sie die folgenden Informationen aus dem Abschnitt „antragsteller“ dieses Belegbildes:
    - antragsteller name
    - antragsteller address
    - antragsteller Kontaktnummer
    
    Formatieren Sie die Antwort streng als JSON-Objekt mit diesen Feldern.
    """
    
    # Create payload for Ollama API
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "images": [base64_image],
        "stream": False
    }
    
    # Send request to Ollama API
    try:
        response = requests.post('http://localhost:11434/api/generate', json=payload)
        print(response.json())
        if response.status_code == 200:
            result = response.json()
            model_response = result.get('response', 'No response from model')
            parsed = safe_json_parse(model_response)
            # If parsed is a dict with 'Antragsteller', return its value
            if isinstance(parsed, dict) and 'Antragsteller' in parsed:
                return parsed['Antragsteller']
            return parsed
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image with Llama 3.2 Vision
        extraction_result = extract_receipt_info(file_path)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'extraction_result': extraction_result
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True) 