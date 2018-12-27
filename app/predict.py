import os
import sys
from yolo import YOLO
from PIL import Image
import io

MODEL_DIR = '/usr/src/app/yolov3-coco'
MODEL_PATH = os.path.join(MODEL_DIR, 'yolov3_coco.h5')
CLASSES_PATH = os.path.join(MODEL_DIR, 'coco_classes.txt')
ANCHORS_PATH = os.path.join(MODEL_DIR, 'yolo_anchors.txt')

params = {
    "model_path": MODEL_PATH,
    "anchors_path": ANCHORS_PATH,
    "classes_path": CLASSES_PATH,
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

