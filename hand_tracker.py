import cv2
import mediapipe as mp
import numpy as np
from config import *

class HandTracker:
    def __init__(self):
        """Initialize MediaPipe hand tracking"""
        # solutions.hands is a template that contains the class Hands and HandLandmark
        self.mp_hands = mp.solutions.hands
        # Hands is a class that defines functions to process the result
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            model_complexity=MODEL_COMPLEXITY,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self, image):
        """Process frame with Mediapipe Solutions task hands"""
        return self.hands.process(image)
    
    def get_paddle_position(self, results):
        """Extract paddle position from hand landmarks"""
        index_finger = self.mp_hands.HandLandmark.INDEX_FINGER_TIP
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]  # Get the first hand detected
            
            # Fetch the coordinates from the Hand Landmark results
            paddle_x = int(hand.landmark[index_finger].x * VIDEO_X)
            paddle_y = int(hand.landmark[index_finger].y * VIDEO_Y)
            # Return as a tuple
            return (paddle_x, paddle_y)
        
        return None 