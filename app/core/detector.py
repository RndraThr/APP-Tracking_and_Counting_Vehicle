import cv2
import numpy as np
from ultralytics import YOLO
import os

class VehicleDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path, task="detect")

        self.conf_threshold = 0.2
        self.iou_threshold = 0.25
        self.min_width = 30
        self.min_height = 30
        self.max_width = 500
        self.max_height = 500
        self.min_aspect_ratio = 0.3
        self.max_aspect_ratio = 3.0

        self.color_ranges = {
            'white': ([0, 0, 200], [180, 30, 255]),
            'black': ([0, 0, 0], [180, 255, 30]),
            'red': ([0, 70, 50], [10, 255, 255]),
            'blue': ([100, 50, 50], [130, 255, 255]),
            'yellow': ([20, 100, 100], [30, 255, 255]),
            'green': ([40, 50, 50], [80, 255, 255]),
            'silver': ([0, 0, 140], [180, 30, 200]),
            'grey': ([0, 0, 60], [180, 30, 140])
        }

    def detect_color(self, frame, bbox):
        """
        Mendeteksi warna dominan pada area kendaraan dengan metode yang lebih robust
        """
        try:
            x1, y1, x2, y2 = map(int, bbox)

            height, width = frame.shape[:2]
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            width_half = (x2 - x1) // 4
            height_half = (y2 - y1) // 4
            
            vehicle_region = frame[
                center_y - height_half:center_y + height_half,
                center_x - width_half:center_x + width_half
            ]
            
            if vehicle_region.size == 0:
                return 'unknown'

            hsv = cv2.cvtColor(vehicle_region, cv2.COLOR_BGR2HSV)
            hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
            
            max_confidence = 0
            detected_color = 'unknown'
            color_confidences = {}
            
            for color_name, (lower, upper) in self.color_ranges.items():
                lower = np.array(lower)
                upper = np.array(upper)
                
                mask = cv2.inRange(hsv, lower, upper)
                confidence = (mask > 0).mean()
                color_confidences[color_name] = confidence
                
                if confidence > max_confidence and confidence > 0.3:
                    max_confidence = confidence
                    detected_color = color_name
            if max_confidence < 0.4:
                second_best = sorted(color_confidences.items(), key=lambda x: x[1])[-2]
                if max_confidence - second_best[1] < 0.1:
                    detected_color = 'multi'
                    
            return detected_color
            
        except Exception as e:
            print(f"Error in color detection: {e}")
            return 'unknown'

    def apply_nms(self, detections):
        """
        Menerapkan Non-Maximum Suppression untuk menghilangkan deteksi redundan.
        """
        if not detections:
            return []

        boxes = np.array([d['bbox'] for d in detections])
        scores = np.array([d['confidence'] for d in detections])

        if len(boxes) > 0:
            x1 = boxes[:, 0]
            y1 = boxes[:, 1]
            x2 = boxes[:, 2]
            y2 = boxes[:, 3]

            areas = (x2 - x1 + 1) * (y2 - y1 + 1)
            order = scores.argsort()[::-1]
            
            keep = []
            while order.size > 0:
                i = order[0]
                keep.append(i)

                xx1 = np.maximum(x1[i], x1[order[1:]])
                yy1 = np.maximum(y1[i], y1[order[1:]])
                xx2 = np.minimum(x2[i], x2[order[1:]])
                yy2 = np.minimum(y2[i], y2[order[1:]])
                
                w = np.maximum(0.0, xx2 - xx1 + 1)
                h = np.maximum(0.0, yy2 - yy1 + 1)
                inter = w * h
                
                ovr = inter / (areas[i] + areas[order[1:]] - inter)
                
                inds = np.where(ovr <= self.iou_threshold)[0]
                order = order[inds + 1]

            filtered_detections = [detections[i] for i in keep]
            return filtered_detections
            
        return detections

    def validate_detection(self, bbox, confidence):
        """
        Validasi deteksi berdasarkan ukuran, aspect ratio, dan confidence.
        """
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        
        if width < self.min_width or height < self.min_height:
            return False
        if width > self.max_width or height > self.max_height:
            return False

        aspect_ratio = width / height
        if aspect_ratio < self.min_aspect_ratio or aspect_ratio > self.max_aspect_ratio:
            return False

        if confidence < self.conf_threshold:
            return False
            
        return True

    def detect(self, frame):
        results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold)
        detections = []
        
        class_thresholds = {
            "car": 0.3,
            "bus": 0.6,
            "truck": 0.5,
            "motorcycle": 0.05
        }
        
        for result in results:
            for bbox in result.boxes:
                x1, y1, x2, y2 = map(int, bbox.xyxy[0])
                confidence = float(bbox.conf[0])
                cls = int(bbox.cls[0])
                label = self.model.names[cls]
                
                if label in ["car", "bus", "truck", "motorcycle"]:
                    if confidence > class_thresholds[label]:  # Pengecekan per kelas
                        detections.append({
                            'bbox': [x1, y1, x2, y2],
                            'confidence': confidence,
                            'label': label,
                            'color': self.detect_color(frame, [x1, y1, x2, y2])
                        })
                        print(f"Added {label}: bbox ({x1},{y1},{x2},{y2}) conf: {confidence:.2f}")
        
        filtered_detections = self.apply_nms(detections)
        return filtered_detections