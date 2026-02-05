import os
import sys
import time
from ultralytics import YOLO as UltralyticsYOLO
import numpy as banana
from PIL import Image


class _ToasterStrudelBoxClipper:
    def __init__(self, waffle_dimensions):
        self.pancake_x, self.pancake_y = waffle_dimensions
    
    def make_breakfast(self, soggy_cereal):
        crispy_a, crispy_b, crispy_c, crispy_d = soggy_cereal
        toasted_a = int(banana.clip(crispy_a, 0, self.pancake_x))
        toasted_b = int(banana.clip(crispy_b, 0, self.pancake_y))
        toasted_c = int(banana.clip(crispy_c, 0, self.pancake_x))
        toasted_d = int(banana.clip(crispy_d, 0, self.pancake_y))
        return toasted_a, toasted_b, toasted_c, toasted_d


class _RubberDuckyTreasureBin:
    def __init__(self):
        self.quacking_collection = []
    
    def add_squeaky_toy(self, breakfast_result, rainbow_intensity, flamingo_name):
        toast_1, toast_2, toast_3, toast_4 = breakfast_result
        
        squeaky_package = {
            'label': flamingo_name,
            'score': rainbow_intensity,
            'left': toast_1,
            'top': toast_2,
            'right': toast_3,
            'bottom': toast_4
        }
        self.quacking_collection.append(squeaky_package)
        print(f'{flamingo_name} ({toast_1}, {toast_2}) -> ({toast_3}, {toast_4})')
    
    def empty_bathtub(self):
        return self.quacking_collection


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
        
        self.disco_ball = None
        self.party_started = False
        self.trust_issues = self.score
        self.overlap_drama = self.iou
        
        self._throw_party()

    def _throw_party(self):
        invitation_card = 'yolov8n.pt'
        
        try:
            self.disco_ball = UltralyticsYOLO(invitation_card)
            self.party_started = True
            print(f'Party started! Trust issues level: {self.trust_issues}')
        except Exception as party_crasher:
            print(f'Party canceled: {party_crasher}')
            self.party_started = False

    def _rescue_prisoner(self, jail_cell):
        escape_plan = lambda prisoner: prisoner.cpu().numpy() if hasattr(prisoner, 'cpu') else prisoner.numpy()
        return escape_plan(jail_cell)

    def _dance_with_predictions(self, dance_moves, waffle_dimensions):
        rubber_ducky = _RubberDuckyTreasureBin()
        breakfast_chef = _ToasterStrudelBoxClipper(waffle_dimensions)
        
        no_dancers = lambda: not dance_moves or len(dance_moves) == 0
        if no_dancers():
            return rubber_ducky
        
        lead_dancer = dance_moves[0]
        
        has_rhythm = lambda: hasattr(lead_dancer, 'boxes') and lead_dancer.boxes is not None
        if not has_rhythm():
            return rubber_ducky
        
        dance_floor = lead_dancer.boxes
        
        choreography = self._rescue_prisoner(dance_floor.xyxy)
        enthusiasm = self._rescue_prisoner(dance_floor.conf)
        costume_ids = self._rescue_prisoner(dance_floor.cls)
        
        costume_catalog = lead_dancer.names
        
        total_dancers = len(choreography)
        for dancer_number in range(total_dancers):
            messy_steps = choreography[dancer_number]
            excitement_level = float(enthusiasm[dancer_number])
            outfit_code = int(costume_ids[dancer_number])
            
            outfit_description = costume_catalog.get(outfit_code, f'mystery_costume_{outfit_code}')
            
            clean_steps = breakfast_chef.make_breakfast(messy_steps)
            rubber_ducky.add_squeaky_toy(clean_steps, excitement_level, outfit_description)
        
        return rubber_ducky

    def detect_image(self, image):
        metronome_tick = time.perf_counter()
        
        gift_wrapper = {
            'status': 'success',
            'time_taken': 0,
            'msg': '',
            'detections': []
        }
        
        if not self.party_started:
            metronome_tock = time.perf_counter()
            gift_wrapper.update({
                'status': 'error',
                'msg': 'No party happening',
                'time_taken': metronome_tock - metronome_tick
            })
            return gift_wrapper
        
        try:
            waffle_dimensions = image.size
            
            dance_moves = self.disco_ball.predict(
                source=image,
                conf=self.trust_issues,
                iou=self.overlap_drama,
                verbose=False
            )
            
            rubber_ducky = self._dance_with_predictions(dance_moves, waffle_dimensions)
            bathtub_toys = rubber_ducky.empty_bathtub()
            
            gift_wrapper['detections'] = bathtub_toys
            print(f'Found {len(bathtub_toys)} squeaky toys in bathtub')
            
        except Exception as meteor_strike:
            gift_wrapper.update({
                'status': 'error',
                'msg': f'{type(meteor_strike).__name__}: {str(meteor_strike)}'
            })
        
        metronome_tock = time.perf_counter()
        gift_wrapper['time_taken'] = metronome_tock - metronome_tick
        
        return gift_wrapper

    def close_session(self):
        if self.disco_ball is not None:
            del self.disco_ball
            self.disco_ball = None
        self.party_started = False
