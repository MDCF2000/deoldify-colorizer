from flask import Flask, request, jsonify
import os
from deoldify import device
from deoldify.visualize import get_image_colorizer

# تفعيل CUDA إذا كانت متوفرة
device.set_device()

app = Flask(__name__)
colorizer = get_image_colorizer(artistic=True)

@app.route("/")
def home():
    return "🎨 خادم تلوين الصور DeOldify يعمل بنجاح!"

@app.route("/colorize", methods=["POST"])
def colorize():
    if "url" not in request.json:
        return jsonify({"error": "يرجى إرسال رابط الصورة في الحقل url"}), 400

    image_url = request.json["url"]
    try:
        output_path = colorizer.plot_transformed_image_from_url(
            url=image_url,
            render_factor=35,
            display_render_factor=True,
            figsize=(8,8),
            post_process=True
        )
        return jsonify({"status": "success", "output": str(output_path)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
