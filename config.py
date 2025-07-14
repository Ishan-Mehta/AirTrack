"""Game Configuration Constants"""

# Video dimensions
VIDEO_X, VIDEO_Y = 640, 480

# Target settings
TARGET_SIZE = 30
NUM_TARGETS = 4

# Game settings
GAME_DURATION = 30  # seconds

# Physics settings
INITIAL_PUCK_VELOCITY = [10, 10]
INCREASE_SPEED_FACTOR = 1
PUCK_RADIUS = 12
PUCK_SMOOTHING_FACTOR = 0.7
PADDLE_RADIUS = 16
PADDLE_SMOOTHING_FACTOR = 0.90

# Text
FONT_SCALE = 0.75
LARGE_FONT_SCALE = 2.0
FONT_THICKNESS = 2
BOLD_FONT_THICKNESS = 3
TEXT_COLOR = (0, 0, 0)  # Black
WHITE_TEXT = (255, 255, 255)  # White
RED_TEXT = (0, 0, 255)  # Red
GREEN_TEXT = (0, 200, 0)  # Green
SEMI_TRANSPARENT_BLACK = (0, 0, 0, 128)  # For overlay backgrounds (if needed)

# Colors (BGR format for OpenCV)
PUCK_COLOR = [255, 0, 0]  # Blue
PADDLE_COLOR = [0, 255, 0]  # Green

# Hand tracking settings
MAX_NUM_HANDS = 1
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5