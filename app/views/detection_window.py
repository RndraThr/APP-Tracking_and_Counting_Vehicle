import cv2
import numpy as np
from datetime import datetime
import time
import os
import torch
from pathlib import Path
import tkinter as tk
from ..core.detector import VehicleDetector
from ..core.tracker import VehicleTracker
from ..core.counter import VehicleCounter
from ..database.repository import VehicleRepository

class DetectionWindow:
    def __init__(self, video_path, location):
        """
        Inisialisasi sistem deteksi kendaraan dengan optimasi performa.
        """
        self.video_path = video_path
        self.location = location
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            gpu_name = torch.cuda.get_device_name()
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"Using GPU: {gpu_name} with {gpu_memory:.2f}GB memory")
            self.batch_size = 1 if gpu_memory < 4 else 2
        else:
            print("GPU not detected. Using CPU for processing.")
            self.batch_size = 1

        self.frame_skip = 1 if torch.cuda.is_available() else 2
        self.detection_threshold = 0.3 if torch.cuda.is_available() else 0.4
        self.frame_width = 640
        self.frame_height = 360
        self.frame_skip = 2
        self.video_speed = 1.5
        self.frame_count = 0
        self.detection_threshold = 0.4
        self.tracking_memory = {}
        self.classification_history = {}
        self.tracked_vehicles = set()
        self.vehicles_tracked = set()
        self.total_count = 0
        self.drawing = False
        self.vertical_lines = []
        self.temp_line = None
        self.vehicle_counts = {
            'car': 0,
            'truck': 0,
            'bus': 0,
            'motorcycle': 0
        }
        
        try:
            self.setup_components()
            self.setup_video_capture()
            self.setup_video_writer()
            self.drawing = False
            self.lines = []
            self.x3, self.y3, self.x4, self.y4 = -1, -1, -1, -1
            self.setup_display()

            if not self.verify_database_connection():
                raise Exception("Failed to establish database connection")
                
            if not os.path.exists(video_path):
                raise Exception(f"Video file not found: {video_path}")
                
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def setup_components(self):
        """
        Inisialisasi model deteksi dan komponen terkait.
        """
        try:
            model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "yolov8n.onnx")
            self.detector = VehicleDetector(model_path)
            self.tracker = VehicleTracker(
                frame_width=self.frame_width,
                frame_height=self.frame_height
            )

            self.counter = VehicleCounter()
            self.repository = VehicleRepository(
                host="localhost",
                user="root",
                password="",
                database="vehicle_db"
            )
        except Exception as e:
            print(f"Error initializing components: {e}")
            raise

    # def setup_video_capture(self):
    #     """
    #     Konfigurasi video capture dengan pengaturan optimal untuk performa.
    #     """
    #     self.cap = cv2.VideoCapture(self.video_path)
    #     self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
    #     self.process_width = 640
    #     self.process_height = 360
    #     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.process_width)
    #     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.process_height)
    #     self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
    #     self.last_process_time = time.time()


    def setup_video_capture(self):
        """
        Konfigurasi video capture dengan support untuk RTSP.
        """
        try:
            is_rtsp = self.video_path.lower().startswith(('rtsp://', 'rtmp://', 'http://'))
            
            if is_rtsp:
                self.cap = cv2.VideoCapture(self.video_path)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                self.cap.set(cv2.CAP_PROP_RTSP_TRANSPORT, cv2.CAP_RTSP_TCP)
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
            else:
                self.cap = cv2.VideoCapture(self.video_path)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
            if not self.cap.isOpened():
                raise Exception(f"Failed to open video source: {self.video_path}")

            self.process_width = 640
            self.process_height = 360
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.process_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.process_height)
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            if is_rtsp and self.fps == 0:
                self.fps = 30            
            self.last_process_time = time.time()
            
        except Exception as e:
            print(f"Error in setup_video_capture: {e}")
            raise
    

    def setup_video_writer(self):
        """
        Setup video writer dengan codec yang kompatibel.
        """
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"detection_{timestamp}.avi")
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(
            output_path,
            fourcc,
            self.fps,
            (self.frame_width, self.frame_height),
            isColor=True
        )
        
        if not self.video_writer.isOpened():
            raise Exception("Failed to initialize video writer")
        
        print(f"Video will be saved to: {output_path}")
        
    def verify_database_connection(self):
        """
        Memverifikasi koneksi database aktif dan berfungsi.
        """
        try:
            if hasattr(self.repository, 'db_available') and self.repository.db_available:
                self.repository.cursor.execute("SELECT 1")
                print("Database connection verified successfully")
                return True
            else:
                print("Database not available. Using API only mode.")
                return True
        except Exception as e:
            print(f"Database connection error: {str(e)}. Using API only mode.")
            return True
        
    def draw_vehicle_box(self, frame, bbox, track_id, vehicle_type, speed, direction, color):
        """
        Menggambar bounding box dan label kendaraan dengan warna yang menyesuaikan tipe kendaraan.
        """
        try:
            x1, y1, x2, y2 = bbox
            colors = {
                'car': (0, 255, 0),
                'truck': (0, 0, 255),
                'bus': (255, 0, 0),
                'motorcycle': (255, 255, 0)
            }
            box_color = colors.get(vehicle_type, (255, 255, 255))
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
            label = f"ID:{track_id} {vehicle_type} {speed}km/h"
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, 
                        (x1, y1 - 25), 
                        (x1 + label_width + 10, y1), 
                        box_color,
                        -1)
            cv2.putText(frame, 
                    label, 
                    (x1 + 5, y1 - 7),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6,  
                    (0, 0, 0),
                    2)  
                    
        except Exception as e:
            print(f"Error drawing box: {e}")
    
    def setup_display(self):
        """
        Konfigurasi tampilan window dan parameter visual.
        """
        cv2.namedWindow("Smart Counting v.4")
        cv2.setMouseCallback("Smart Counting v.4", self.draw_line)
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.line_type = 2
        
        self.vehicle_colors = {
            'car': (0, 255, 0),
            'truck': (255, 0, 0),
            'bus': (0, 0, 255),
            'motorcycle': (255, 255, 0)
        }
        
        self.line_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.overlay_color = (0, 0, 0)
        self.overlay_alpha = 0.3

    # def draw_line(self, event, x, y, flags, param):
    #     """
    #     Handler untuk input mouse dalam menggambar garis.
    #     """
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         self.drawing = True
    #         self.x3, self.y3 = x, y
    #     elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
    #         self.x4, self.y4 = x, y
    #     elif event == cv2.EVENT_LBUTTONUP:
    #         self.drawing = False
    #         self.x4, self.y4 = x, y
    #         self.lines.append(((self.x3, self.y3), (self.x4, self.y4)))
    
    def draw_line(self, event, x, y, flags, param):
        """
        Handler untuk input mouse dalam menggambar satu garis vertikal dinamis.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            # Reset daftar garis dan tambahkan garis baru
            self.vertical_lines = [x]
            
    def validate_vehicle_class(self, bbox, label):
        """
        Validasi tambahan berdasarkan ukuran kendaraan
        """
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / height if height != 0 else 0
        if label == "bus":
            return width > 100 and height > 120 and aspect_ratio > 1.2
        elif label == "truck":
            return width > 100 and height > 100 and aspect_ratio > 1.5
        elif label == "motorcycle":
            return width < 100 and height < 120 and aspect_ratio < 1.2
        elif label == "car":
            return 50 < width < 150 and 50 < height < 120
        
        return True
    
    def validate_detection(self, detection):
        """
        Validasi deteksi untuk mengurangi false positives.
        """
        x1, y1, x2, y2 = detection['bbox']
        width = x2 - x1
        height = y2 - y1
        
        min_size = 30
        min_ratio = 0.2
        max_ratio = 5.0
        
        if width < min_size or height < min_size:
            return False
            
        ratio = width / height
        if ratio < min_ratio or ratio > max_ratio:
            return False
            
        return True

    def process_frame(self, frame):
        try:
            frame_resized = cv2.resize(frame, (self.frame_width, self.frame_height))
            self._draw_reference_lines(frame_resized)
            detections = self.detector.detect(frame_resized)
            tracks = self.tracker.update(detections)
            current_frame_vehicles = self._process_tracks(tracks, frame_resized)
            self._update_statistics(current_frame_vehicles)
            self.draw_statistics(frame_resized)
            self.video_writer.write(frame_resized)
            
            return frame_resized
            
        except Exception as e:
            print(f"Error in process_frame: {e}")
            return frame

    # def _draw_reference_lines(self, frame):
    #     """
    #     Menggambar garis referensi pada frame.
    #     """
    #     try:
    #         middle_x = self.frame_width // 2
    #         cv2.line(frame, (middle_x, 0), (middle_x, self.frame_height), 
    #                 (255, 255, 0), 2)  # Warna kuning untuk garis vertikal
            
    #         cv2.putText(frame, "Lajur Kanan", (middle_x + 10, 30), 
    #                     self.font, self.font_scale * 1.2, self.text_color, 
    #                     self.line_type)
    #         cv2.putText(frame, "Lajur Kiri", (225, 30), 
    #                     self.font, self.font_scale * 1.2, self.text_color, 
    #                     self.line_type)
            
    #         counting_line_y = int(self.frame_height * 0.5)
    #         cv2.line(frame, (0, counting_line_y), 
    #                 (self.frame_width, counting_line_y), 
    #                 (0, 0, 255), 2)  # Warna merah untuk garis horizontal
                    
    #         print(f"Drawing reference lines: middle_x={middle_x}, counting_line_y={counting_line_y}")
                    
    #     except Exception as e:
    #         print(f"Error drawing reference lines: {e}")

    
    def _draw_reference_lines(self, frame):
        """
        Menggambar garis referensi pada frame dengan satu garis vertikal dinamis.
        """
        try:
            counting_line_y = int(self.frame_height * 0.5)
            cv2.line(frame, (0, counting_line_y), 
                    (self.frame_width, counting_line_y), 
                    (0, 0, 255), 2)

            if self.vertical_lines:
                x_pos = self.vertical_lines[-1]
                cv2.line(frame, (x_pos, 0), (x_pos, self.frame_height), 
                        (255, 255, 0), 2)  # Warna kuning
                
                cv2.putText(frame, "Lajur Kanan", (x_pos + 10, 30), 
                            self.font, self.font_scale * 1.2, self.text_color, 
                            self.line_type)
                cv2.putText(frame, "Lajur Kiri", (x_pos - 100, 30), 
                            self.font, self.font_scale * 1.2, self.text_color, 
                            self.line_type)
                        
        except Exception as e:
            print(f"Error drawing reference lines: {e}")
    
    
    def _check_line_crossing(self, y1, y2):
        """
        Memeriksa crossing dengan margin yang lebih besar
        """
        counting_line_y = int(self.frame_height * 0.5)
        margin = 25
        detection_zone = (counting_line_y - margin, counting_line_y + margin)

        if y1 <= counting_line_y <= y2:
            vehicle_height = y2 - y1
            center_y = (y1 + y2) / 2
            if abs(center_y - counting_line_y) < margin:
                return True
        
        return False

    def _process_tracks(self, tracks, frame):
        """
        Memproses semua tracks yang terdeteksi dalam frame saat ini.
        """
        current_frame_vehicles = set()
        detections = self.detector.detect(frame)

        active_tracks = {}
        
        for track in tracks:
            try:
                x1, y1, x2, y2, track_id = map(int, track)
                track_bbox = [x1, y1, x2, y2]
                center = ((x1 + x2) // 2, (y1 + y2) // 2)

                print(f"\nProcessing track {track_id}")
                print(f"Position: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

                too_close = False
                for other_id, other_center in active_tracks.items():
                    dist = np.sqrt((center[0] - other_center[0])**2 + (center[1] - other_center[1])**2)
                    if dist < 30:
                        too_close = True
                        break
                        
                if too_close:
                    continue
                        
                active_tracks[track_id] = center
                speed = self.counter.calculate_speed(track_id, center[0], center[1])
                # direction = "kanan" if center[0] > self.frame_width//2 else "kiri"
                direction = self._get_direction(center[0])

                best_iou = 0
                best_detection = None
                
                for det in detections:
                    det_bbox = det['bbox']
                    iou = self._calculate_iou(track_bbox, det_bbox)
                    if iou > best_iou and iou > 0.13:
                        best_iou = iou
                        best_detection = det

                if best_detection:
                    vehicle_type = best_detection['label']
                    if track_id not in self.classification_history:
                        self.classification_history[track_id] = {}
                    if vehicle_type in ['bus', 'truck']:
                        self.classification_history[track_id][vehicle_type] = self.classification_history[track_id].get(vehicle_type, 0) + 1
                        if len(self.classification_history[track_id]) > 0:
                            vehicle_type = max(self.classification_history[track_id].items(), key=lambda x: x[1])[0]
                    color = best_detection.get('color', 'unknown')
                else:
                    vehicle_type = self.tracking_memory.get(track_id, {}).get('type', 'car')
                    color = self.tracking_memory.get(track_id, {}).get('color', 'unknown')

                if track_id not in self.tracking_memory:
                    self.tracking_memory[track_id] = {
                        'first_seen': self.frame_count,
                        'last_seen': self.frame_count,
                        'counted': False,
                        'type': vehicle_type,
                        'color': color,
                        'speed': speed,
                        'direction': direction,
                        'center': center
                    }
                else:
                    self.tracking_memory[track_id].update({
                        'last_seen': self.frame_count,
                        'type': vehicle_type,
                        'speed': speed,
                        'direction': direction,
                        'center': center
                    })

                if not self.tracking_memory[track_id]['counted']:
                    crossing_detected = self._check_line_crossing(y1, y2)
                    print(f"Crossing check for track {track_id}: {crossing_detected}")
                    
                    if crossing_detected:
                        self.tracking_memory[track_id]['counted'] = True
                        current_frame_vehicles.add((track_id, direction))
                        print(f"Added vehicle {track_id} to current frame vehicles")

                        self.save_vehicle_data(
                            track_id,
                            vehicle_type,
                            speed,
                            direction,
                            track_bbox,
                            color
                        )

                self.draw_vehicle_box(
                    frame, 
                    track_bbox,
                    track_id,
                    vehicle_type,
                    speed,
                    direction,
                    color
                )
                
            except Exception as e:
                print(f"Error processing track {track_id}: {e}")
                continue
        
        print(f"Current frame vehicles: {current_frame_vehicles}")
        return current_frame_vehicles
    
    def _get_direction(self, center_x):
        if not self.vertical_lines:
            return "kanan" if center_x > self.frame_width//2 else "kiri"

        nearest_line = min(self.vertical_lines, key=lambda x: abs(x - center_x))
        return "kanan" if center_x > nearest_line else "kiri"
    
    # def _process_tracks(self, tracks, frame):
    #     current_frame_vehicles = set()
    #     active_tracks = {} 
    #     detections = self.detector.detect(frame)
    #     tracks_with_area = []
    #     for track in tracks:
    #         x1, y1, x2, y2, track_id = map(int, track)
    #         area = (x2 - x1) * (y2 - y1)
    #         tracks_with_area.append((track, area))
        
    #     tracks_with_area.sort(key=lambda x: x[1], reverse=True)
        
    #     for track, area in tracks_with_area:
    #         try:
    #             x1, y1, x2, y2, track_id = map(int, track)
    #             track_bbox = [x1, y1, x2, y2]
    #             center = ((x1 + x2) // 2, (y1 + y2) // 2)
    #             best_detection = None
    #             best_iou = 0
                
    #             for det in detections:
    #                 iou = self._calculate_iou(track_bbox, det['bbox'])
    #                 if iou > best_iou:
    #                     best_iou = iou
    #                     best_detection = det
                
    #             too_close = False
    #             for other_id, other_info in active_tracks.items():
    #                 other_center = other_info['center']
    #                 other_bbox = other_info['bbox']
                    
    #                 dist = np.sqrt((center[0] - other_center[0])**2 + 
    #                             (center[1] - other_center[1])**2)
    #                 iou = self._calculate_iou(track_bbox, other_bbox)
                    
    #                 if dist < 40 or iou > 0.25:
    #                     too_close = True
    #                     break
                
    #             if too_close:
    #                 continue  # Langsung skip jika terlalu dekat
                
    #             active_tracks[track_id] = {
    #                 'center': center,
    #                 'bbox': track_bbox
    #             }
    #             speed = self.counter.calculate_speed(track_id, center[0], center[1])
    #             direction = "kanan" if center[0] > self.frame_width//2 else "kiri"
    #             vehicle_type = best_detection['label'] if best_detection else 'car'
    #             if track_id not in self.tracking_memory:
    #                 self.tracking_memory[track_id] = {
    #                     'first_seen': self.frame_count,
    #                     'last_seen': self.frame_count,
    #                     'counted': False,
    #                     'type': vehicle_type,
    #                     'speed': speed,
    #                     'direction': direction,
    #                     'center': center,
    #                     'bbox': track_bbox,
    #                     'prev_bbox': track_bbox,  # Simpan bbox sebelumnya
    #                     'stable_count': 0  # Counter untuk stabilitas
    #                 }
    #             else:
    #                 prev_track = self.tracking_memory[track_id]
    #                 bbox_change = sum(abs(a - b) for a, b in zip(track_bbox, prev_track['bbox']))

    #                 if bbox_change > 100 and prev_track['stable_count'] > 5:
    #                     track_bbox = prev_track['bbox']
    #                 else:
    #                     track_bbox = [
    #                         int(0.8 * curr + 0.2 * prev)
    #                         for curr, prev in zip(track_bbox, prev_track['bbox'])
    #                     ]
    #                     prev_track['stable_count'] += 1
                    
    #                 self.tracking_memory[track_id].update({
    #                     'last_seen': self.frame_count,
    #                     'speed': speed,
    #                     'direction': direction,
    #                     'center': center,
    #                     'bbox': track_bbox,
    #                     'prev_bbox': prev_track['bbox'],  # Update prev_bbox
    #                     'type': vehicle_type
    #                 })

    #             if not self.tracking_memory[track_id]['counted']:
    #                 if self._check_line_crossing(y1, y2):
    #                     if self.tracking_memory[track_id]['stable_count'] >= 3:
    #                         self.tracking_memory[track_id]['counted'] = True
    #                         current_frame_vehicles.add((track_id, direction))

    #             self.draw_vehicle_box(
    #                 frame,
    #                 track_bbox,  # Gunakan bbox yang sudah dismooth
    #                 track_id,
    #                 self.tracking_memory[track_id]['type'],
    #                 speed,
    #                 direction,
    #                 self.tracking_memory[track_id].get('color', 'unknown')
    #             )
                
    #         except Exception as e:
    #             print(f"Error processing track {track_id}: {e}")
    #             continue
        
    #     return current_frame_vehicles

    def _get_vehicle_type(self, bbox):
        """
        Menentukan tipe kendaraan berdasarkan ukuran bbox
        """
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        area = width * height
        ratio = width / height
        
        if area > 5000 and ratio > 0.8:
            return 'bus'
        elif area > 3000:
            return 'truck'
        elif area < 1500 and ratio < 0.7:
            return 'motorcycle'
        else:
            return 'car'
    
    def _calculate_iou(self, bbox1, bbox2):
        """
        Menghitung Intersection over Union antara dua bounding box
        """
        x1 = max(bbox1[0], bbox2[0])
        y1 = max(bbox1[1], bbox2[1])
        x2 = min(bbox1[2], bbox2[2])
        y2 = min(bbox1[3], bbox2[3])
        
        if x2 < x1 or y2 < y1:
            return 0.0
            
        intersection = (x2 - x1) * (y2 - y1)
        
        area1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        area2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
        
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0
    
    def _update_statistics(self, current_frame_vehicles):
        """
        Update statistik counting berdasarkan kendaraan yang terdeteksi
        """
        print(f"Updating statistics for vehicles: {current_frame_vehicles}")
        
        for track_id, direction in current_frame_vehicles:
            self.total_count += 1
            vehicle_type = self.tracking_memory[track_id].get('type', 'car')
            self.vehicle_counts[vehicle_type] += 1
            print(f"Updated count for {vehicle_type}: {self.vehicle_counts[vehicle_type]}")
    
    def cleanup_tracking_memory(self, current_ids):
        """
        Membersihkan tracking memory dengan lebih agresif dan efisien
        """
        memory_timeout = 30
        current_time = time.time()
        
        if not hasattr(self, 'last_cleanup'):
            self.last_cleanup = current_time

        if current_time - self.last_cleanup > 5:
            inactive_ids = []
            for track_id in self.tracking_memory:
                if track_id not in current_ids:
                    if self.frame_count - self.tracking_memory[track_id]['last_seen'] > memory_timeout:
                        inactive_ids.append(track_id)
            
            for track_id in inactive_ids:
                del self.tracking_memory[track_id]
                if hasattr(self, 'classification_history') and track_id in self.classification_history:
                    del self.classification_history[track_id]
            
            self.last_cleanup = current_time

    def check_line_crossing(self, y1, y2, line_y):
        """
        Memeriksa apakah kendaraan melintasi garis penghitung.
        """
        return y2 > line_y > y1

    def draw_statistics(self, frame):
        """
        Menampilkan statistik kendaraan pada frame dengan tampilan yang lebih compact.
        """
        overlay_height = 100
        overlay_width = 150
        padding = 5
        overlay = frame[0:overlay_height, 0:overlay_width].copy()
        cv2.rectangle(frame, (0, 0), (overlay_width, overlay_height), 
                    (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame[0:overlay_height, 0:overlay_width], 0.7, 0, 
                        frame[0:overlay_height, 0:overlay_width])

        font = cv2.FONT_HERSHEY_SIMPLEX
        title_scale = 0.45
        text_scale = 0.4
        font_thickness = 1
        title_color = (255, 255, 255)
        value_colors = {
            'total': (255, 255, 255),
            'car': (0, 255, 0),
            'truck': (0, 0, 255),
            'bus': (255, 0, 0),
            'motorcycle': (255, 255, 0)
        }

        x = padding
        y = 15

        cv2.putText(frame, f"Total Vehicles: {self.total_count}", 
                    (x, y), font, title_scale, title_color, font_thickness)

        y += 15
        cv2.putText(frame, f"Cars: {self.vehicle_counts['car']}", 
                    (x, y), font, text_scale, value_colors['car'], font_thickness)
        
        y += 15
        cv2.putText(frame, f"Trucks: {self.vehicle_counts['truck']}", 
                    (x, y), font, text_scale, value_colors['truck'], font_thickness)
        
        y += 15
        cv2.putText(frame, f"Buses: {self.vehicle_counts['bus']}", 
                    (x, y), font, text_scale, value_colors['bus'], font_thickness)
        
        y += 15
        cv2.putText(frame, f"Motorcycles: {self.vehicle_counts['motorcycle']}", 
                    (x, y), font, text_scale, value_colors['motorcycle'], font_thickness)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_size = cv2.getTextSize(timestamp, font, 0.5, 1)[0]
        timestamp_x = frame.shape[1] - timestamp_size[0] - padding
        timestamp_y = frame.shape[0] - padding
        
        cv2.putText(frame, timestamp, (timestamp_x, timestamp_y),
                    font, 0.5, (255, 255, 255), 1)

    def save_vehicle_data(self, track_id, vehicle_type, speed, direction, bbox, color):
        """
        Menyimpan data kendaraan ke database.
        """
        try:
            koordinat = f"({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]})"
            timestamp = datetime.now()
            
            print(f"Saving data: ID={track_id}, Type={vehicle_type}, Speed={speed}, Direction={direction}, Color={color}")
            
            success = self.repository.save_vehicle(
                vehicle_id=str(track_id),
                klasifikasikendaraan=vehicle_type,
                timestamp=timestamp,
                drivingspeed=float(speed),
                drivingdirection=direction,
                koordinat=koordinat,
                warna=color,
                lokasisurvey=self.location
            )
            
            if not success:
                print(f"Failed to save vehicle data for ID: {track_id}")
                
        except Exception as e:
            print(f"Error saving to database: {str(e)}")

    # def run(self):
    #     """
    #     Menjalankan proses deteksi dan tracking dengan optimasi performa.
    #     """
    #     try:
    #         frame_time = 1.0 / self.fps
    #         while True:
    #             loop_start = time.time()
                
    #             ret, frame = self.cap.read()
    #             if not ret:
    #                 break
                
    #             self.frame_count += 1
    #             if self.frame_count % self.frame_skip != 0:
    #                 continue
                
    #             # Process frame
    #             processed_frame = self.process_frame(frame)
                
    #             # Display dengan frame rate control
    #             cv2.imshow("Smart Counting v.4", processed_frame)
                
    #             # Kontrol frame rate
    #             elapsed = time.time() - loop_start
    #             wait_time = max(1, int((frame_time - elapsed) * 1000))
    #             if cv2.waitKey(wait_time) & 0xFF == ord('q'):
    #                 break
                    
    #             # Sleep untuk mengurangi penggunaan CPU
    #             if elapsed < frame_time:
    #                 time.sleep(frame_time - elapsed)
                
    #             key = cv2.waitKey(wait_time) & 0xFF
    #             if key == ord('q'):
    #                 break
    #             elif key == ord('c'):  # Clear vertical lines
    #                 self.vertical_lines = []    
    #     except Exception as e:
    #         print(f"Error in main loop: {e}")
    #     finally:
    #         self.cleanup()
    
    
    # def run(self):
    #     """
    #     Menjalankan proses deteksi dan tracking dengan support RTSP.
    #     """
    #     try:
    #         is_rtsp = self.video_path.lower().startswith(('rtsp://', 'rtmp://', 'http://'))
    #         frame_time = 1.0 / self.fps
    #         frame_count = 0
    #         retry_count = 0
    #         max_retries = 3
            
    #         while True:
    #             try:
    #                 loop_start = time.time()
                    
    #                 ret, frame = self.cap.read()
    #                 if not ret:
    #                     if is_rtsp:
    #                         print("Lost connection, attempting to reconnect...")
    #                         retry_count += 1
    #                         if retry_count > max_retries:
    #                             print("Max retries exceeded")
    #                             break

    #                         self.cap.release()
    #                         time.sleep(1)
    #                         self.setup_video_capture()
    #                         continue
    #                     else:
    #                         break

    #                 retry_count = 0
    #                 frame_count += 1
    #                 if frame_count % self.frame_skip != 0:
    #                     continue

    #                 processed_frame = self.process_frame(frame)
    #                 cv2.imshow("Smart Counting v.4", processed_frame)

    #                 elapsed = time.time() - loop_start
    #                 wait_time = max(1, int((frame_time - elapsed) * 1000))
    #                 key = cv2.waitKey(wait_time) & 0xFF
    #                 if key == ord('q'):
    #                     print("Exiting...")
    #                     break
    #                 elif key == ord('c'):
    #                     print("Clearing vertical lines...")
    #                     self.vertical_lines = []
    #                 elif key == ord('p'):
    #                     print("Paused. Press any key to continue...")
    #                     cv2.waitKey(-1)
    #                 if elapsed < frame_time:
    #                     time.sleep(frame_time - elapsed)
                        
    #             except Exception as e:
    #                 print(f"Error in frame processing: {e}")
    #                 if is_rtsp:
    #                     continue
    #                 else:
    #                     break
                        
    #     except Exception as e:
    #         print(f"Error in main loop: {e}")
    #     finally:
    #         self.cleanup()
    
    
    def run(self):
        try:
            is_rtsp = self.video_path.lower().startswith(('rtsp://', 'rtmp://', 'http://'))
            frame_time = 1.0 / self.fps
            frame_count = 0
            retry_count = 0
            max_retries = 3
            
            while True:
                try:
                    loop_start = time.time()
                    
                    ret, frame = self.cap.read()
                    if not ret:
                        if is_rtsp:
                            print("Lost connection, attempting to reconnect...")
                            retry_count += 1
                            if retry_count > max_retries:
                                print("Max retries exceeded")
                                break

                            self.cap.release()
                            time.sleep(1)
                            self.setup_video_capture()
                            continue
                        else:
                            break

                    retry_count = 0
                    frame_count += 1
                    if frame_count % self.frame_skip != 0:
                        continue

                    processed_frame = self.process_frame(frame)
                    cv2.imshow("Smart Counting v.4", processed_frame)

                    elapsed = time.time() - loop_start
                    wait_time = max(1, int((frame_time - elapsed) * 1000))
                    key = cv2.waitKey(wait_time) & 0xFF
                    if key == ord('q'):
                        print("Exiting...")
                        break
                    elif key == ord('c'):
                        print("Clearing vertical lines...")
                        self.vertical_lines = []
                    elif key == ord('p'):
                        print("Paused. Press any key to continue...")
                        cv2.waitKey(-1)
                    if elapsed < frame_time:
                        time.sleep(frame_time - elapsed)
                        
                except Exception as e:
                    print(f"Error in frame processing: {e}")
                    if is_rtsp:
                        continue
                    else:
                        break
                        
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.cleanup()
            cv2.destroyAllWindows()
            import sys
            root = tk.Tk()
            root.withdraw()
            root.after(100, root.destroy)
            root.mainloop()
    
    def _write_frame_to_buffer(self, frame):
        """
        Menulis frame ke buffer untuk meningkatkan performa writing.
        """
        self.writer_buffer.append(frame)
        
        if len(self.writer_buffer) >= self.max_buffer_size:
            self._flush_buffer()

    def _flush_buffer(self):
        """
        Flush buffer ke video writer.
        """
        for frame in self.writer_buffer:
            self.video_writer.write(frame)
        self.writer_buffer.clear()
    
    # def cleanup(self):
    #     """
    #     Membersihkan resources dengan proper buffer handling.
    #     """
    #     try:
    #         if hasattr(self, 'writer_buffer') and self.writer_buffer:
    #             self._flush_buffer() 
    #         if hasattr(self, 'cap'):
    #             self.cap.release()
    #         if hasattr(self, 'video_writer'):
    #             self.video_writer.release()
    #         if hasattr(self, 'repository'):
    #             self.repository.close()
    #         self.tracking_memory.clear()
    #         self.classification_history.clear()
            
    #         cv2.destroyAllWindows()
    #     except Exception as e:
    #         print(f"Error in cleanup: {e}")
    
    def cleanup(self):
        try:
            if hasattr(self, 'writer_buffer') and self.writer_buffer:
                self._flush_buffer() 
            if hasattr(self, 'cap'):
                self.cap.release()
            if hasattr(self, 'video_writer'):
                self.video_writer.release()
            if hasattr(self, 'repository'):
                self.repository.close()
            self.tracking_memory.clear()
            self.classification_history.clear()
            
            cv2.destroyAllWindows()
            for i in range(5):
                cv2.waitKey(1)
        except Exception as e:
            print(f"Error in cleanup: {e}")