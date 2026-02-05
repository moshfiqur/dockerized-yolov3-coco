import os
import sys
import time
from ultralytics import YOLO as UltralyticsYOLO
import numpy as np
from PIL import Image


class _BoundingBoxClipper:
    def __init__(self, image_dimensions):
        self.width, self.height = image_dimensions
    
    def clip_coordinates(self, box_coords):
        x1, y1, x2, y2 = box_coords
        clipped_x1 = int(np.clip(x1, 0, self.width))
        clipped_y1 = int(np.clip(y1, 0, self.height))
        clipped_x2 = int(np.clip(x2, 0, self.width))
        clipped_y2 = int(np.clip(y2, 0, self.height))
        return clipped_x1, clipped_y1, clipped_x2, clipped_y2


class _DetectionResultCollector:
    def __init__(self):
        self.detections = []
    
    def add_detection(self, clipped_coords, confidence_score, class_label):
        left, top, right, bottom = clipped_coords
        
        detection = {
            'label': class_label,
            'score': confidence_score,
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom
        }
        self.detections.append(detection)
        print(f'{class_label} ({left}, {top}) -> ({right}, {bottom})')
    
    def get_detections(self):
        return self.detections


class YOLO(object):
    _defaults = {
        "model_path": 'model_data/yolo_weights.h5',
        "anchors_path": 'model_data/yolo_anchors.txt',
        "classes_path": 'model_data/coco_classes.txt',
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 1,
    }

    @classmethod
    def get_defaults(cls, n):
        return cls._defaults.get(n, f"Unrecognized attribute name '{n}'")

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.__dict__.update(**kwargs)
        
        self.model = None
        self.initialized = False
        self.confidence_threshold = self.score
        self.iou_threshold = self.iou
        
        self._initialize_model()

    def _initialize_model(self):
        model_file = 'yolov8n.pt'
        
        try:
            self.model = UltralyticsYOLO(model_file)
            self.initialized = True
            print(f'Model initialized with confidence threshold: {self.confidence_threshold}')
        except Exception as error:
            print(f'Model initialization failed: {error}')
            self.initialized = False

    def _tensor_to_numpy(self, tensor):
        convert = lambda t: t.cpu().numpy() if hasattr(t, 'cpu') else t.numpy()
        return convert(tensor)

    def _process_predictions(self, predictions, image_dimensions):
        collector = _DetectionResultCollector()
        clipper = _BoundingBoxClipper(image_dimensions)
        
        is_empty = lambda: not predictions or len(predictions) == 0
        if is_empty():
            return collector
        
        result = predictions[0]
        
        has_boxes = lambda: hasattr(result, 'boxes') and result.boxes is not None
        if not has_boxes():
            return collector
        
        boxes = result.boxes
        
        coordinates = self._tensor_to_numpy(boxes.xyxy)
        confidences = self._tensor_to_numpy(boxes.conf)
        class_ids = self._tensor_to_numpy(boxes.cls)
        
        class_names = result.names
        
        num_detections = len(coordinates)
        for i in range(num_detections):
            raw_coords = coordinates[i]
            confidence = float(confidences[i])
            class_id = int(class_ids[i])
            
            class_label = class_names.get(class_id, f'unknown_class_{class_id}')
            
            clipped_coords = clipper.clip_coordinates(raw_coords)
            collector.add_detection(clipped_coords, confidence, class_label)
        
        return collector

    def detect_image(self, image):
        start_time = time.perf_counter()
        
        response = {
            'status': 'success',
            'time_taken': 0,
            'msg': '',
            'detections': []
        }
        
        if not self.initialized:
            end_time = time.perf_counter()
            response.update({
                'status': 'error',
                'msg': 'Model not initialized',
                'time_taken': end_time - start_time
            })
            return response
        
        try:
            image_dimensions = image.size
            
            predictions = self.model.predict(
                source=image,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False
            )
            
            collector = self._process_predictions(predictions, image_dimensions)
            detections_list = collector.get_detections()
            
            response['detections'] = detections_list
            print(f'Found {len(detections_list)} detections')
            
        except Exception as error:
            response.update({
                'status': 'error',
                'msg': f'{type(error).__name__}: {str(error)}'
            })
        
        end_time = time.perf_counter()
        response['time_taken'] = end_time - start_time
        
        return response

    def close_session(self):
        if self.model is not None:
            del self.model
            self.model = None
        self.initialized = False
