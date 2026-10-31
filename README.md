# Dental Cavity Detection — Vercel frontend

**Huzaifa Saeeed · su92-bscsm-f23-538 · Deep Learning**

A responsive static HTML/CSS/JavaScript interface for a three-category enamel
caries classification semester project. This package supplies the missing home
page and explicit static output settings. It works without Python on Vercel.

## Quick deployment

1. Extract the ZIP and open `Dental_Cavity_Vercel`.
2. Upload its **contents** to your GitHub repository root, preserving `public/`.
   `vercel.json` must be beside `public/`, not inside it. Commit the changes.
3. Import that repository into Vercel. Select **Other**, Root Directory **./**,
   an empty Build Command, an empty Install Command, and Output Directory **public**.
   The included `vercel.json` supplies these deployment overrides.
4. Redeploy after saving the settings. The home page is `public/index.html`.

If you upload the outer folder too, set Root Directory to `Dental_Cavity_Vercel`.
For an existing mixed Python repository, placing this entire package in a
`website/` subfolder and setting Root Directory to `website` keeps the frontend
deployment isolated. Do not use `python build.py` for this static frontend.

See `DEPLOY_INSTRUCTIONS.txt` for Roman Urdu instructions and 404 checks.

## Included features

- Accessible, responsive interface; no frontend package installation or CDN dependency.
- JPG/PNG/WEBP preview, drag-and-drop, clear/change controls, type/size validation.
- Three source-labelled sample photos. Labels are not substituted for predictions.
- Real API integration with health checks, class-order validation, model scores,
  loading/error states, stale-request cancellation and JSON result download.
- Report, PowerPoint and Colab notebook downloads.
- Verified preparation counts and dataset source attribution.

**Model weights and full-run evaluation results are not included.** The page
explicitly shows “Model not connected” and disables analysis until a compatible
real model service is ready. The interface does not generate simulated scores.
The published GitHub/weights/YouTube links stay inactive until configured.

## Set your public project links

Edit `public/assets/config.js`, using your own real HTTPS URLs:

```js
window.DENTAL_CONFIG = Object.freeze({
  apiBaseUrl: "", // base URL of your separately deployed model API
  githubUrl: "",
  weightsUrl: "", // direct download of actual full-run weights or training output
  youtubeUrl: "",
});
```

These settings are public. Never place an API secret or private token here.
No website login is required for this academic demonstration.

## Connect your actual trained model (optional)

The frontend is static; uploading `.keras`, `.h5` or `.ipynb` files to Vercel does
not execute a model. `optional_backend/` contains a separate FastAPI service for
the complete inference export produced by the supplied Colab notebook.

1. Finish the full training run. Extract `Dental_Cavity_Training_Output.zip`.
2. Copy **dental_caries.keras** and **class_names.json** into
   `optional_backend/model/`. Do not use only a weights file or a smoke-test model.
3. Run the service locally from `optional_backend/` in Python 3.12:

```bash
python -m venv .venv
# Activate .venv using your operating system's activation command.
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

For local frontend testing from the package root:

```bash
python -m http.server 8000 --directory public
```

Set `apiBaseUrl` to `http://localhost:8001` for that local test. Production
requires an HTTPS model service reachable by visitors, not your localhost.

For a Docker-capable Python host, use `optional_backend/` as its build context:

```bash
docker build -t dental-model optional_backend
docker run -p 7860:7860 \
  -e ALLOWED_ORIGINS=https://YOUR-ACTUAL-SITE.vercel.app dental-model
```

Replace the origin with your exact frontend URL (no trailing slash). The API
needs TensorFlow memory and startup time; deploy it on a suitable Python/Docker
service independently. No external backend deployment has been performed here.
Set the backend's `ALLOWED_ORIGINS` to the Vercel frontend origin, and then set
the frontend's `apiBaseUrl` to the backend HTTPS base URL. Commit and redeploy.

If you keep trained files out of Git, mount them on the backend and set
`MODEL_PATH` and `CLASSES_PATH`. The supplied `.gitignore` excludes local model
files by default. The optional backend is excluded from this static Vercel upload.
If the course requires downloadable weights, publish the real weights separately
in your project repository/release and configure `weightsUrl`.

### API contract

`GET /health` returns `ready: true` only after the model has loaded and its output
contract has been checked. `POST /predict` accepts a multipart field called `file`.
Both responses carry `class_names` in this exact order:

```json
["no_enamel_caries", "early_stage_enamel_caries", "advanced_enamel_caries"]
```

`POST /predict` additionally returns `scores`, a three-number softmax vector in
the same order. Scores must be finite, within [0, 1], and sum approximately to 1.
There is no fake prediction fallback.

The complete `.keras` inference model embeds resizing to 224×224 and MobileNetV2
scaling. The API passes RGB float32 pixels in **0–255**, without dividing by 255.
It calls the model with `training=False` and does not persist uploaded images.
The API is an academic example without authentication, quotas or production
traffic controls; configure those at your chosen host before broader use.

## Dataset and evidence

Source: **Caries-Spectra V2**, Galib Muhammad Shahriar Himel, Md Masudul Islam and
Ummae Hamida Hannan, Mendeley Data, version 2, 2023, **CC BY 4.0**.

https://data.mendeley.com/datasets/9jnf2jvghy/2

The source publishes 2,000 top-level photographs. Removing 249 exact duplicate
copies retains 1,751 images: 398 no-enamel-caries, 679 early-stage and 674 advanced.
The fixed partition contains 1,220 training, 269 validation and 262 test images.
Recorded similarity groups do not cross splits, but patient independence has not
been established. Photographs keep their original bytes and publisher labels;
the sample filenames are renamed. `public/assets/samples/source_information.json`
records their source paths. Source authors do not endorse this project.

The report and presentation describe the current implementation and distinguish
verified dataset preparation from pending full training metrics. Update them with
the actual `metrics.json` after training; no accuracy is assumed in this package.

## Scope

Educational research prototype for close-up tooth RGB photographs and image-level
source labels. It does not localize lesions, classify X-rays or provide a dental
diagnosis. Early-stage enamel caries need not imply a visible cavity. Model scores
are not calibrated disease probabilities; clinical performance is unvalidated.

## Vercel reference

https://vercel.com/docs/builds/configure-a-build

https://vercel.com/docs/project-configuration/vercel-json
