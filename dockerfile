# -------- Stage 1: build & install Python deps --------
FROM python:3.11-slim AS builder

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

# System packages often needed by Torch / diffusers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only files needed to resolve dependencies first
COPY dev-requirements.txt ./dev-requirements.txt
# If you create a dedicated requirements.txt later, copy that here too
RUN pip install --upgrade pip \
 && pip install fastapi uvicorn[standard] pillow diffusers torch transformers

# -------- Stage 2: runtime image --------
FROM python:3.11-slim

# Copy installed site‑packages from builder
COPY --from=builder /usr/local /usr/local
WORKDIR /app

# Copy rest of the source code
COPY . .

# Expose the port FastAPI will listen on
EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
