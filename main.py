from flask import Flask, request, send_file
import torch
from deoldify import device
from deoldify.visualize import get_image_colorizer
import tempfile
import urllib.request
from PIL import Image
import os

app = Flask(__name__)
colorizer = get_image_colorizer(artistic=True)

@app.route('/')
def home():
    return "🎨 DeOldify Colorizer API - استخدم ?url= لرابط الصورة القديمة"

@app.route('/colorize')
def colorize():
    url = request.args.get('url')
    if not url:
        return "❌ Missing ?url= parameter", 400

    # تحميل الصورة من الإنترنت
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    urllib.request.urlretrieve(url, tmp.name)

    # تلوين الصورة
    result_path = colorizer.get_transformed_image(
        path=tmp.name,
        render_factor=35,
        post_process=True
    )

    return send_file(result_path, mimetype="image/jpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
