FROM python:3.11-slim

# Install Tesseract OCR and required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY . .

# Render provides PORT automatically
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT}