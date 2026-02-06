FROM python:3.11-slim

LABEL maintainer="Moshfiqur Rahman <rahman.moshfiqur@gmail.com>"
LABEL description="Modern YOLO object detection service"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

EXPOSE 10080

CMD ["gunicorn", "serve:app", "-c", "/usr/src/app/gunicorn_config.py"]