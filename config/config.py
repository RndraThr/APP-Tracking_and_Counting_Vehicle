class Config:
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "vehicle_db"
    MODEL_PATH = "models/yolov8n.onnx" 
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_SKIP = 2
    MAX_AGE = 30
    MIN_HITS = 3
    IOU_THRESHOLD = 0.3
