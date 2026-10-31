from pathlib import Path
import argparse, json
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps

def predict_image(image_path):
    root = Path(__file__).resolve().parent
    names = json.loads((root / 'class_names.json').read_text())
    model = tf.keras.models.load_model(root / 'dental_caries.keras', compile=False)
    with Image.open(image_path) as image:
        rgb = ImageOps.exif_transpose(image).convert('RGB')
        batch = np.asarray(rgb, dtype=np.float32)[None, ...]
    scores = model(batch, training=False).numpy()[0]
    result = {'label':names[int(scores.argmax())], 'model_score':float(scores.max()),
              'scores':dict(zip(names, map(float, scores))),
              'note':'Educational image classifier. Not a clinically validated diagnosis.'}
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image', type=Path)
    args = parser.parse_args()
    print(json.dumps(predict_image(args.image), indent=2))
