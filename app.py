from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import os

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Load OCR model

@app.route('/')
def home():
    return "🚀 PaddleOCR API is running!"

@app.route('/ocr', methods=['POST'])
def run_ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = 'temp_image.jpg'
    file.save(filepath)

    result = ocr.ocr(filepath, cls=True)
    text_lines = [line[1][0] for line in result[0]]

    os.remove(filepath)
    return jsonify({'extracted_text': text_lines})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
