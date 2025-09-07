from flask import Flask, request, render_template, send_file
import os
from led_detection import process_image  # ✅ Import process_image from led_detect.py
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if not uploaded_file:
            return "No file uploaded", 400

        input_image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(input_image_path)

         # ✅ Handle .webp
        if uploaded_file.filename.lower().endswith(".webp"):
            
            im = Image.open(input_image_path).convert("RGB")
            converted_image_path = input_image_path.replace(".webp", ".png")
            im.save(converted_image_path)
            input_image_path = converted_image_path
        
        output_image_path = os.path.join(OUTPUT_FOLDER, "led_detection_result.png")
        output_text_path = os.path.join(OUTPUT_FOLDER, "led_detection_results.txt")

        try:
            process_image(input_image_path, output_image_path, output_text_path)
            
            # Read the output text file
            with open(output_text_path, "r") as f:
                text_content = f.read()

            return render_template("result.html", image_path=output_image_path, text_content=text_content)
        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html")

@app.route("/download/<path:filename>")
def download(filename):
    """ Allows users to download the processed image and text results. """
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

