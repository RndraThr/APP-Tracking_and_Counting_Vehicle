class Config:
    # Database configuration
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "vehicle_db"
    
    # Model configuration
    MODEL_PATH = "models/yolov8n.onnx"
    
    # Detection configuration
    CONFIDENCE_THRESHOLD = 0.3
    FRAME_SKIP = 2
    
    # Tracker configuration
    MAX_AGE = 30
    MIN_HITS = 3
    IOU_THRESHOLD = 0.3
