from datetime import datetime, timedelta
import time

class VehicleCounter:
    def __init__(self):
        self.vehicles_tracked = set()
        self.vehicle_speeds = {}
        self.count = 0
        self.pixel_to_meter = 0.2
        self.speed_history = {}    
        self.speed_window = 5    
        self.last_speed = {}       
        self.smooth_factor = 0.3

    def calculate_datetime(self, frame_number, fps, start_time):
        seconds = frame_number / fps
        time_delta = timedelta(seconds=seconds)
        return start_time + time_delta

    def calculate_speed(self, track_id, center_x, center_y):
        """
        Menghitung kecepatan dengan smoothing yang lebih baik
        """
        current_time = time.time()
        
        if track_id in self.vehicle_speeds:
            prev_x, prev_y, prev_time = self.vehicle_speeds[track_id]
            
            # Hitung jarak
            distance_px = ((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2) ** 0.5
            time_diff = current_time - prev_time if prev_time else 1e-6
            
            # Konversi ke kecepatan
            speed_px_per_sec = distance_px / time_diff
            speed_mps = speed_px_per_sec * self.pixel_to_meter
            speed_kmph = speed_mps * 3.6
            
            # Smooth speed dengan exponential moving average
            if track_id in self.last_speed:
                prev_speed = self.last_speed[track_id]
                smoothed_speed = (self.smooth_factor * speed_kmph + 
                                (1 - self.smooth_factor) * prev_speed)
            else:
                smoothed_speed = speed_kmph
            
            # Update history
            self.last_speed[track_id] = smoothed_speed
            self.vehicle_speeds[track_id] = (center_x, center_y, current_time)
            
            # Minimal speed untuk menghindari nilai 0
            return max(int(smoothed_speed), 1)
            
        # Inisialisasi untuk track baru
        self.vehicle_speeds[track_id] = (center_x, center_y, current_time)
        self.last_speed[track_id] = 0
        return 1