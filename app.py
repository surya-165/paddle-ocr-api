from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import tempfile
import os

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr_image():
    try:
        # Check if a file is provided
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        # Perform OCR
        text = pytesseract.image_to_string(Image.open(tmp_path))

        os.remove(tmp_path)

        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
