from ultralytics import YOLO
import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, model_path="yolov8n.pt"):
        logger.info(f"Loading YOLO model: {model_path}")
        self.model = YOLO(model_path)

    def infer(self, frame):
        # Run inference
        results = self.model(frame, verbose=False)
        return results[0] # Return first result (single frame)
