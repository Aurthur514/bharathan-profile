import cv2
import time
from typing import Generator, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self, rtsp_url: str):
        self.rtsp_url = rtsp_url
        self.cap = None
        self.reconnect_delay = 5  # seconds
        self.last_frame_time = 0

    def connect(self):
        if self.cap is not None:
            self.cap.release()
        logger.info(f"Connecting to {self.rtsp_url}...")
        self.cap = cv2.VideoCapture(self.rtsp_url)
        if not self.cap.isOpened():
            logger.error(f"Failed to open stream {self.rtsp_url}")
            return False
        return True

    def get_frame(self) -> Tuple[bool, Optional[cv2.typing.MatLike]]:
        if self.cap is None or not self.cap.isOpened():
            if not self.connect():
                time.sleep(self.reconnect_delay)
                return False, None

        ret, frame = self.cap.read()
        if not ret:
            logger.warning(f"Failed to read frame from {self.rtsp_url}. Reconnecting...")
            self.cap.release()
            return False, None

        self.last_frame_time = time.time()
        return True, frame

    def release(self):
        if self.cap:
            self.cap.release()
