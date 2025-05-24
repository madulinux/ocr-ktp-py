from flask import Flask, request, jsonify
import os
from utils.ktp_ocr import KtpOcr
from utils.image_helper import KtpImageProcess

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"})


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@app.route("/ocr/ktp", methods=["POST"])
def ocr_ktp():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]

    try:
        # Read the image file
        image_request_bytes = image_file.read()

        # Process the image
        image_process = KtpImageProcess(image_request_bytes).run()

        # Perform OCR on the processed image
        score, content = KtpOcr(image_process).run() or (0, {})

        # Return the results
        return jsonify({"success": True, "score": score, "content": content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Check if Google Cloud credentials are set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        )
        print("The OCR functionality requires Google Cloud Vision API credentials.")

    # Get configuration from environment variables with defaults
    port = int(os.environ.get('PORT', 5001))
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
