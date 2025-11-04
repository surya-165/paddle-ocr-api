from flask import Flask, request, jsonify
import easyocr
import tempfile
import os

app = Flask(__name__)

# Initialize EasyOCR reader once (to avoid reloading each time)
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/')
def home():
    return jsonify({"message": "EasyOCR API is running!"})

@app.route('/ocr', methods=['POST'])
def run_ocr():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file uploaded"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # Run OCR
        results = reader.readtext(temp_path)

        # Clean up
        os.remove(temp_path)

        # Extract text only (ignore bounding boxes and confidence)
        extracted_text = " ".join([res[1] for res in results])

        return jsonify({
            "text": extracted_text,
            "details": [
                {"bbox": res[0], "text": res[1], "confidence": res[2]}
                for res in results
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
