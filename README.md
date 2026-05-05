# Dockerized YOLO Object Detection Service

A containerized object detection REST API powered by [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics), served via [Gunicorn](https://gunicorn.org/). The YOLOv8n model weights are downloaded automatically on the first run.

- **Model:** YOLOv8n (Ultralytics)
- **Runtime:** Python 3.13 (slim)
- **Server:** Gunicorn WSGI
- **Port:** 10080

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/) 20.10 or newer

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/moshfiqur/dockerized-yolo.git
cd dockerized-yolo
```

### 2. Build the Docker image

```bash
docker build -t dockerized-yolo .
```

### 3. Run the service

The object detection model requires a minimum of 4 GB of memory. The `-m 4g` flag ensures Docker allocates enough.

```bash
docker run -p 10080:10080 -m 4g dockerized-yolo
```

The API will be available at `http://localhost:10080`.

**Optional — interactive shell (for debugging):**

```bash
docker run -it -p 10080:10080 -m 4g dockerized-yolo bash
```

---

## Usage

Send a `multipart/form-data` POST request with an image attached under the field name `file`.

### Using `curl`

```bash
curl -X POST http://localhost:10080 \
     -F "file=@/path/to/your/image.jpg"
```

### Using PHP

A sample PHP script [`uploader.php`](uploader.php) is included that sends a POST request with a local image file to the running service.

---

## API Response

On success the service returns a JSON object:

```json
{
    "status": "success",
    "time_taken": 1.234,
    "msg": "",
    "detections": [
        {
            "label": "person",
            "score": 0.9987449645996094,
            "left": 98,
            "top": 101,
            "right": 1025,
            "bottom": 935
        },
        {
            "label": "chair",
            "score": 0.582422137260437,
            "left": 74,
            "top": 602,
            "right": 421,
            "bottom": 904
        }
    ]
}
```

| Field | Description |
|---|---|
| `status` | `"success"` or `"error"` |
| `time_taken` | Inference time in seconds |
| `msg` | Error message (empty on success) |
| `detections` | Array of detected objects |
| `detections[].label` | Class name (e.g. `"person"`, `"car"`) |
| `detections[].score` | Confidence score (0–1) |
| `detections[].left/top/right/bottom` | Bounding box pixel coordinates |

On error (e.g. no file uploaded), the service returns HTTP `400 Bad Request` with a plain-text error description.

---

## Configuration

| Parameter | Default | Description |
|---|---|---|
| Confidence threshold | `0.30` | Minimum detection confidence |
| IoU threshold | `0.45` | Non-maximum suppression overlap threshold |
| Workers | `2` | Number of Gunicorn worker processes |
| Timeout | `30 s` | Gunicorn worker timeout |

These can be adjusted in [`app/predict.py`](app/predict.py) and [`app/gunicorn_config.py`](app/gunicorn_config.py).

---

## License

This project is licensed under the [MIT License](LICENSE).
```