from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Paddle OCR API is running"

@app.route('/ocr', methods=['POST'])
def run_ocr():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            filepath = tmp.name
            file.save(filepath)

        # Create a lightweight OCR instance for this request
        # use_gpu=False to stay compatible with Render free tier
        ocr = PaddleOCR(lang='en', use_gpu=False)

        # Perform OCR
        result = ocr.ocr(filepath)

        # Extract text lines from OCR output
        extracted_text = []
        for line in result:
            for _, (text, confidence) in line:
                extracted_text.append(text)

        # Clean up temporary file
        os.remove(filepath)

        return jsonify({
            'success': True,
            'extracted_text': extracted_text
        })

    except Exception as e:
        # Log the error for debugging
        print(f"❌ Error during OCR: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run on Render with proper binding
    app.run(host='0.0.0.0', port=10000)
