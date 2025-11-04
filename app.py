from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Tesseract OCR API running (optimized for Render Free Tier)"

@app.route('/ocr', methods=['POST'])
def ocr_route():
    try:
        # Ensure a file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        uploaded_file = request.files['file']

        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            temp_path = tmp.name
            uploaded_file.save(temp_path)

        # Run OCR using Tesseract
        text = pytesseract.image_to_string(Image.open(temp_path))

        # Clean up temp file
        os.remove(temp_path)

        # Convert text into clean list of lines
        extracted_lines = [line.strip() for line in text.splitlines() if line.strip()]

        return jsonify({
            'success': True,
            'lines_detected': len(extracted_lines),
            'extracted_text': extracted_lines
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
