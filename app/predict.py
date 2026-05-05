import sys
from yolo import YOLO
from PIL import Image
import io

params = {
    "score" : 0.3,
    "iou" : 0.45,
    "model_image_size" : (416, 416),
    "gpu_num" : 1
}

yolo_obj = YOLO(**params)

def predict(image):
    try:
        image = Image.open(io.BytesIO(image))
        detections = yolo_obj.detect_image(image)
        return detections
    except Exception:
        exc_type, value, traceback = sys.exc_info()
        return exc_type.__name__+': '+str(value)

