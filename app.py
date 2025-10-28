from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import os
import tempfile

app = Flask(__name__)

# ✅ Load OCR model once when the app starts
# (this takes a few seconds on the first request only)
ocr = PaddleOCR(lang='en')

@app.route('/')
def home():
    return "✅ Paddle OCR API is running (optimized for Render Free Tier)"

@app.route('/ocr', methods=['POST'])
def run_ocr():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            filepath = tmp.name
            file.save(filepath)

        # Perform OCR using the preloaded model
        result = ocr.ocr(filepath)

        # Extract text
        extracted_text = []
        for page in result:
            for line in page:
                text, confidence = line[1]
                extracted_text.append(text)

        # Delete temp file
        os.remove(filepath)

        return jsonify({
            'success': True,
            'lines_detected': len(extracted_text),
            'extracted_text': extracted_text
        })

    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run on Render default port
    app.run(host='0.0.0.0', port=10000)
