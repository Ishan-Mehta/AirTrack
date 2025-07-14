import cv2
from config import *

class Camera:
    def __init__(self, camera_index=0):
        """Initialize camera capture"""
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_X)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_Y)

        actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Actual resolution: {actual_width} x {actual_height}")
        
    def read_frame(self):
        """Read a frame from the camera"""
        success, frame = self.cap.read()
        if not success:
            return None, False
        
        # Flip frame horizontally for selfie view
        frame = cv2.flip(frame, 1)
        return frame, True
    
    def convert_to_rgb(self, frame):
        """Convert BGR frame to RGB"""
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    def convert_to_bgr(self, frame):
        """Convert RGB frame to BGR for display"""
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)