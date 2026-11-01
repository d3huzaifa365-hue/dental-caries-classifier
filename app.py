"""Dental Cavity Detection: web app (page + model backend in one Flask app).

Routes:
  GET  /             the web page
  GET  /api/health   tells the page the model is ready
  POST /api/predict  runs the trained MobileNetV2 model on an uploaded photo
"""
from pathlib import Path
import io
import json

import numpy as np
from flask import Flask, jsonify, request, send_file
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "model" / "dental.onnx"
CLASS_NAMES = json.loads((ROOT / "model" / "class_names.json").read_text())

MAX_BODY_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 25_000_000
MAX_SIDE = 1600  # the model resizes to 224 anyway; this only protects memory

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_BODY_BYTES

_session = None


def get_session():
    """Load the model once and keep it for later requests."""
    global _session
    if _session is None:
        import onnxruntime as ort
        _session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
    return _session


def classify(data):
    with Image.open(io.BytesIO(data)) as image:
        if image.width * image.height > MAX_PIXELS:
            raise ValueError("Image is too large.")
        rgb = ImageOps.exif_transpose(image).convert("RGB")
    if max(rgb.size) > MAX_SIDE:
        rgb.thumbnail((MAX_SIDE, MAX_SIDE), Image.BILINEAR)
    batch = np.asarray(rgb, dtype=np.float32)[None, ...]  # raw 0..255, as the model expects
    session = get_session()
    scores = session.run(None, {session.get_inputs()[0].name: batch})[0][0]
    return [float(s) for s in scores]


def json_reply(payload, status=200):
    response = jsonify(payload)
    response.status_code = status
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def home():
    return send_file(ROOT / "index.html", mimetype="text/html")


@app.get("/api/health")
def health():
    return json_reply({"ready": MODEL_PATH.exists(), "class_names": CLASS_NAMES})


@app.post("/api/predict")
def predict():
    upload = request.files.get("file")
    if upload is None:
        return json_reply({"error": "No image received."}, 400)
    try:
        scores = classify(upload.read())
    except Exception:
        return json_reply({"error": "Could not read this image."}, 400)
    if len(scores) != len(CLASS_NAMES):
        return json_reply({"error": "Model output does not match the classes."}, 500)
    return json_reply({"class_names": CLASS_NAMES, "scores": scores})


@app.errorhandler(413)
def too_large(_):
    return json_reply({"error": "Image too large."}, 413)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
