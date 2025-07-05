# FastAPI AI Image Generation Service

A lightweight REST API that turns text prompts into images using
`diffusers`/`torch`. Everything is wrapped in a Docker container for easy
deployment anywhere that can run containers.

## ✨ Features
* **/generate** – returns a PNG file  
  `GET /generate?prompt=Two+cats+playing+chess`
* **/generate-memory** – streams the PNG in‑memory (no temp file)  
  `GET /generate-memory?prompt=Cityscape+at+dusk`
* Simple CRUD‑style sample routes (`/`, `/items/{id}`, `/items/`)

## 🐳 Quick start

```bash
# 1. Build the image
docker build -t ai-image-generator .

# 2. Run the container
docker run --rm -p 8000:8000 ai-image-generator
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

## 🚀 Example calls

```bash
# Save an image to disk
curl -o output.png \
  "http://localhost:8000/generate?prompt=A+sunset+over+mountains"

# Stream an image
curl "http://localhost:8000/generate-memory?prompt=Futuristic+bike"
```

## 🛠 Local development
```bash
# Install dev tools
python -m venv .venv && source .venv/bin/activate
pip install -r dev-requirements.txt
pip install fastapi uvicorn[standard] pillow diffusers torch transformers

# Auto‑format, lint, and type‑check
black .               # formatting
ruff check .          # lint
mypy .                # type hints
```
Run locally:

```bash
uvicorn main:app --reload --port 8000
```

## 🏗️ Producing images

The heavy lifting happens inside `ml.obtain_image()`, which should accept:

```python
image = obtain_image(
    prompt,
    num_inference_steps=50,
    seed=None,
    guidance_scale=7.5,
)
```

Make sure your implementation returns a `PIL.Image` instance.

## 📂 Project structure
```
.
├── main.py               # FastAPI routes
├── ml/                   # your ML / diffusion code
│   └── __init__.py
├── dev-requirements.txt  # lint, formatter, typing
└── Dockerfile
```

## ⚖️ License
MIT – do what you want, but no warranty is provided.  
Remember to respect model licenses (e.g., Stable Diffusion) and content
policies when deploying publicly.
