import cv2
import numpy as np
from config import *

class Renderer:
    def __init__(self):
        """Initialize renderer and load target image"""
        self.target_image = self._load_target_image()
        
    def _load_target_image(self):
        """Load and prepare target image"""
        target_image = cv2.resize(cv2.imread('target.png'), (TARGET_SIZE, TARGET_SIZE))
        return cv2.cvtColor(target_image, cv2.COLOR_RGB2RGBA)
    
    def overlay_circle(self, image, obj_position, radius, color):
        """Overlay a circular object on the image"""
        # Extract a square around the center of the object
        obj_roi = image[(obj_position[1] - radius):(obj_position[1] + (radius+1)),
                       (obj_position[0] - radius):(obj_position[0] + (radius+1))]
        
        side_sq = 2 * radius + 1
        
        for y in range(side_sq):
            for x in range(side_sq):
                # Check if pixel lies within the circle
                if ((y-radius)**2 + (x-radius)**2) <= radius**2:
                    obj_roi[y, x] = np.array(color)
    
    def overlay_targets(self, image, targets):
        """Overlay target images on the frame"""
        for target in targets:
            if target.hit:
                continue
                
            # Extract region of interest
            target_roi = image[target.position[1]: (target.position[1] + self.target_image.shape[0]),
                              target.position[0]: (target.position[0] + self.target_image.shape[1])]
            
            # Calculate opacity
            opacity = self.target_image[:, :, 3] / 255.0
            transparency = 1.0 - opacity
            
            # Overlay target image onto frame
            for color_code in range(3):
                target_roi[:, :, color_code] = (
                    opacity * self.target_image[:, :, color_code] +
                    transparency * target_roi[:, :, color_code]
                )
    
    def draw_ui(self, image, score, remaining_time, game_over):
        """Draw UI elements (score and timer) with improved style and clamped positions"""
        # Score (top right)
        score_text = f'Score: {score}'
        (w, h), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)
        score_x = min(max(int(VIDEO_X*0.8), 0), VIDEO_X - w - 20)
        score_y = max(int(VIDEO_Y*0.1), h + 20)
        cv2.putText(image, score_text, (score_x, score_y), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, WHITE_TEXT, FONT_THICKNESS, cv2.LINE_AA)

        # Timer (top center)
        timer_text = f'{round(remaining_time, 2) if not game_over else "--"} secs'
        (tw, th), _ = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)
        timer_x = min(max(int(VIDEO_X*0.5 - tw/2), 0), VIDEO_X - tw - 20)
        timer_y = max(int(VIDEO_Y*0.1), th + 20)
        cv2.putText(image, timer_text, (timer_x, timer_y), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, WHITE_TEXT, FONT_THICKNESS, cv2.LINE_AA)
    
    def draw_game_over(self, image, score):
        """Draw game over screen with big, bold, centered red text and shadow, clamped to image bounds"""
        main_text = 'YOU LOSE!'
        score_text = f'Your Score: {score}'
        (w, h), _ = cv2.getTextSize(main_text, cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, BOLD_FONT_THICKNESS)
        x = max(int((VIDEO_X - w) / 2), 0)
        y = max(int((VIDEO_Y) / 2), h)
        x = min(x, VIDEO_X - w)
        y = min(y, VIDEO_Y - h)
        # Shadow
        cv2.putText(image, main_text, (x+3, y+3), cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, (0,0,0), BOLD_FONT_THICKNESS+2, cv2.LINE_AA)
        # Main
        cv2.putText(image, main_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, RED_TEXT, BOLD_FONT_THICKNESS, cv2.LINE_AA)
        # Score below
        (sw, sh), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, BOLD_FONT_THICKNESS)
        sx = max(int((VIDEO_X - sw) / 2), 0)
        sy = min(y + h + 30, VIDEO_Y - sh)
        cv2.putText(image, score_text, (sx, sy), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, WHITE_TEXT, BOLD_FONT_THICKNESS, cv2.LINE_AA)
    
    def draw_victory(self, image, score, completion_time):
        """Draw victory screen with big, bold, centered green text and show completion time, clamped to image bounds"""
        main_text = 'YOU WON!'
        score_text = f'Your Score: {score}'
        time_text = f'Time: {round(completion_time, 2)}s'
        (w, h), _ = cv2.getTextSize(main_text, cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, BOLD_FONT_THICKNESS)
        x = max(int((VIDEO_X - w) / 2), 0)
        y = max(int((VIDEO_Y) / 2), h)
        x = min(x, VIDEO_X - w)
        y = min(y, VIDEO_Y - h)
        # Shadow
        cv2.putText(image, main_text, (x+3, y+3), cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, (0,0,0), BOLD_FONT_THICKNESS+2, cv2.LINE_AA)
        # Main
        cv2.putText(image, main_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, LARGE_FONT_SCALE, GREEN_TEXT, BOLD_FONT_THICKNESS, cv2.LINE_AA)
        # Score below
        (sw, sh), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, BOLD_FONT_THICKNESS)
        sx = max(int((VIDEO_X - sw) / 2), 0)
        sy = min(y + h + 30, VIDEO_Y - sh)
        cv2.putText(image, score_text, (sx, sy), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, WHITE_TEXT, BOLD_FONT_THICKNESS, cv2.LINE_AA)
        # Time below score
        (tw, th), _ = cv2.getTextSize(time_text, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, BOLD_FONT_THICKNESS)
        tx = max(int((VIDEO_X - tw) / 2), 0)
        ty = min(sy + sh + 20, VIDEO_Y - th)
        cv2.putText(image, time_text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE*2, WHITE_TEXT, BOLD_FONT_THICKNESS, cv2.LINE_AA) 