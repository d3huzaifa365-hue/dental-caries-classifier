# Dental Cavity Detection: website

A web page where anyone can upload a close-up tooth photo and see what the trained MobileNetV2 model predicts (no enamel caries, early-stage enamel caries, or advanced enamel caries).

Educational research prototype. Not a clinically validated diagnosis.

## How it works
- `index.html` is the page.
- `api/health.py` tells the page the model is ready.
- `api/predict.py` receives the photo and runs the trained model (`model/dental.onnx`).
- `model/class_names.json` holds the class order.

## Dataset
Caries-Spectra V2 (Himel, Islam and Hannan, 2023), https://data.mendeley.com/datasets/9jnf2jvghy/2, CC BY 4.0.

## Result
Test accuracy 89.7% on 262 held-out images (image-group holdout; patient independence is not established).

## Deploy
1. Put this whole folder in a public GitHub repository.
2. On vercel.com choose **Add New > Project**, import the repository, and click **Deploy**. No settings need changing.
3. Open the link Vercel gives you.

To show your GitHub, report, presentation and YouTube links on the page, fill them in at the top of the script in `index.html` (the `LINKS` block).
