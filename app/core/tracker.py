# tracker.py
from .sort.sort import Sort
import numpy as np
from collections import deque
import time

class VehicleTracker:
    def __init__(self, frame_width=640, frame_height=360):
        self.tracker = Sort(
            max_age=40,          
            min_hits=1,         
            iou_threshold=0.2
        )
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.track_history = {}
        self.min_track_hits = 1
        self.max_prediction_age = 30
        self.smoothing_window = 3
        self.debug_mode = True
        self.frame_stats = {
            'current_detections': 0,
            'current_tracks': 0,
            'lost_tracks': 0
        }

        self.cumulative_stats = {
            'total_tracked': set(),
            'total_detections': 0,
            'total_lost': 0
        }
        
        self.velocity_history = {}
        self.last_positions = {}
        self.last_update_time = {}

    # def predict_missing_tracks(self, current_tracks, current_time=None):
    #     """
    #     Memprediksi posisi tracks yang hilang berdasarkan velocity history
    #     """
    #     if current_time is None:
    #         current_time = time.time()
            
    #     current_track_ids = {int(track[4]) for track in current_tracks}
    #     predicted_tracks = []
        
    #     for track_id, last_pos in self.last_positions.items():
    #         if track_id not in current_track_ids and track_id in self.velocity_history:
    #             time_since_last_update = current_time - self.last_update_time.get(track_id, 0)
                
    #             # Hanya prediksi jika waktu sejak update terakhir masih dalam batas
    #             if time_since_last_update < self.max_prediction_age:
    #                 velocity = self.velocity_history[track_id]
                    
    #                 # Prediksi posisi baru
    #                 predicted_pos = last_pos + velocity * time_since_last_update
                    
    #                 # Validasi posisi hasil prediksi
    #                 if self._validate_bbox(predicted_pos):
    #                     predicted_tracks.append(np.array([
    #                         *predicted_pos,
    #                         track_id
    #                     ]))
        
    #     return predicted_tracks
    
    def predict_missing_tracks(self, current_tracks, current_time=None):
        if current_time is None:
            current_time = time.time()
                
        current_track_ids = {int(track[4]) for track in current_tracks}
        predicted_tracks = []
        
        for track_id, last_pos in self.last_positions.items():
            if track_id not in current_track_ids and track_id in self.velocity_history:
                time_since_last_update = current_time - self.last_update_time.get(track_id, 0)
                if time_since_last_update < self.max_prediction_age:
                    velocity = self.velocity_history[track_id]
                    predicted_pos = last_pos + velocity * time_since_last_update
                    
                    if self._validate_bbox(predicted_pos):
                        predicted_tracks.append(np.array([
                            *predicted_pos,
                            track_id
                        ]))
        
        return predicted_tracks
    
    def _validate_bbox(self, bbox):
        """
        Validasi bounding box dengan threshold yang lebih longgar
        """
        x1, y1, x2, y2 = bbox
        padding = 20 
        
        if ((-padding <= x1 <= self.frame_width + padding) and 
            (-padding <= y1 <= self.frame_height + padding) and 
            (-padding <= x2 <= self.frame_width + padding) and 
            (-padding <= y2 <= self.frame_height + padding) and 
            x2 > x1 and y2 > y1):
            return True
        return False

    def _update_velocity(self, track_id, current_pos, current_time):
        """
        Update velocity estimation untuk track
        """
        if track_id in self.last_positions:
            last_pos = self.last_positions[track_id]
            last_time = self.last_update_time[track_id]
            time_diff = current_time - last_time
            
            if time_diff > 0:
                velocity = (current_pos - last_pos) / time_diff   
                if track_id in self.velocity_history:
                    alpha = 0.7
                    self.velocity_history[track_id] = (
                        alpha * velocity + 
                        (1 - alpha) * self.velocity_history[track_id]
                    )
                else:
                    self.velocity_history[track_id] = velocity
        
        self.last_positions[track_id] = current_pos
        self.last_update_time[track_id] = current_time

    def update(self, detections):
        try:
            current_time = time.time()
            
            if not detections:
                self.update_statistics([], [])
                return []

            detection_array = np.array([
                [d['bbox'][0], d['bbox'][1], d['bbox'][2], d['bbox'][3], d['confidence']]
                for d in detections
            ])

            tracks = self.tracker.update(detection_array)
            if len(tracks) < len(detections):
                predicted = self.predict_missing_tracks(tracks, current_time)
                if len(predicted) > 0:
                    tracks = np.vstack([tracks, predicted])
            for track in tracks:
                track_id = int(track[4])
                if track_id not in self.track_history:
                    self.track_history[track_id] = deque(maxlen=10)
                self.track_history[track_id].append(track[:4])
            
            return tracks
            
        except Exception as e:
            print(f"Error in tracker update: {e}")
            return np.array([])

    def _ensure_track_consistency(self, tracks):
        """
        Memastikan konsistensi track ID berdasarkan posisi dan ukuran
        """
        consistent_tracks = []
        for track in tracks:
            track_id = int(track[4])
            if track_id in self.track_history:
                last_pos = self.track_history[track_id][-1]
                current_pos = track[:4]
                
                if np.all(np.abs(current_pos - last_pos) < 50):
                    consistent_tracks.append(track)
            else:
                consistent_tracks.append(track)
        
        return np.array(consistent_tracks)
    
    def update_statistics(self, tracks, detections):
        """
        Update statistik tracking
        """
        self.frame_stats['current_detections'] = len(detections)
        self.frame_stats['current_tracks'] = len(tracks)
        self.frame_stats['lost_tracks'] = max(0, 
            self.frame_stats['current_detections'] - self.frame_stats['current_tracks']
        )
        
        self.cumulative_stats['total_detections'] += len(detections)
        self.cumulative_stats['total_lost'] += self.frame_stats['lost_tracks']
        
        for track in tracks:
            self.cumulative_stats['total_tracked'].add(int(track[4]))
        
        if self.debug_mode:
            print("Frame Statistics:", self.frame_stats)
            print("Cumulative Statistics:", {
                'total_unique_tracks': len(self.cumulative_stats['total_tracked']),
                'total_detections': self.cumulative_stats['total_detections'],
                'total_lost': self.cumulative_stats['total_lost']
            })

    def cleanup_old_tracks(self):
        """
        Membersihkan track history yang sudah tidak aktif
        """
        current_time = time.time()
        for track_id in list(self.last_update_time.keys()):
            if current_time - self.last_update_time[track_id] > self.max_prediction_age:
                self.last_positions.pop(track_id, None)
                self.velocity_history.pop(track_id, None)
                self.last_update_time.pop(track_id, None)