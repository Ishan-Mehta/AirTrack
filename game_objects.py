import cv2
import numpy as np
from config import *

class Puck:
    def __init__(self):
        """Initialize puck at center of screen"""
        self.position = np.array([VIDEO_X/2, VIDEO_Y/2]).astype(int)
        self.velocity = np.array(INITIAL_PUCK_VELOCITY)
        self.radius = PUCK_RADIUS
        
    def update_position(self):
        """Update puck position based on velocity and time"""
        # Create new_pos using current position and velocity
        new_pos = np.array(self.position + self.velocity)
        # Smoothen the displacement so that the movement does not appear discrete
        new_pos[0] = (self.position[0] * (1 - PUCK_SMOOTHING_FACTOR) + new_pos[0] * PUCK_SMOOTHING_FACTOR)
        new_pos[1] = (self.position[1] * (1 - PUCK_SMOOTHING_FACTOR) + new_pos[1] * PUCK_SMOOTHING_FACTOR)

        self.position = new_pos.astype(int)
    
    # Acts as a dummy function when factor = 1
    def increase_velocity(self, factor=INCREASE_SPEED_FACTOR):
        """Increase puck velocity by given factor"""
        self.velocity *= factor

class Paddle:
    def __init__(self):
        """Initialize paddle at random position"""
        self.radius = PADDLE_RADIUS
        self.position = tuple((self.radius + 5, self.radius + 5))
        
    def update_position(self, new_position):
        """Update paddle position"""
        # Check if paddle is within bounds
        if new_position:
            # Convert new_position to numpy array if it's a tuple
            new_pos = np.array(new_position)
            # Smoothen the displacement so that the movement does not appear discrete
            new_pos[0] = (self.position[0] * (1 - PADDLE_SMOOTHING_FACTOR) + new_pos[0] * PADDLE_SMOOTHING_FACTOR)
            new_pos[1] = (self.position[1] * (1 - PADDLE_SMOOTHING_FACTOR) + new_pos[1] * PADDLE_SMOOTHING_FACTOR)

            # Check if paddle is within bounds
            new_pos[0] = max(self.radius + 1, min(new_pos[0], VIDEO_X - self.radius - 1))
            new_pos[1] = max(self.radius + 1, min(new_pos[1], VIDEO_Y - self.radius - 1))
            
            # Apply smoothing
            self.position = new_pos.astype(int)
        

class Target:
    def __init__(self, position):
        """Initialize target at given position"""
        self.position = position
        self.hit = False
        self.size = TARGET_SIZE
        
    def is_hit(self, puck):
        """Check if puck is within acceptance region of target"""
        target_center = np.array(self.position) + self.size // 2
        
        # dxy : [dx, dy]
        dxy = abs(target_center - puck.position)
        # [dx - side / 2, dy - side / 2]
        dsx, dsy = dxy - self.size // 2

        # Calculate the puck's nearest distance from the target's boundary
        db = np.sqrt(max(0, dsx) ** 2 + max(0, dsy) ** 2)
        # Calculate the distance between the 2 centers
        distance = np.linalg.norm(puck.position - target_center)

        return db <= puck.radius or distance < self.size // 2

class TargetManager:
    def __init__(self):
        """Initialize target manager with random target positions"""
        self.targets = []
        self._initialize_targets()
        
    def _initialize_targets(self):
        """Create random target positions"""
        # Creates 2D Numpy array (NUM_TARGETS * 2)
        target_positions = np.random.randint(0, [VIDEO_X - TARGET_SIZE, VIDEO_Y - TARGET_SIZE], size=(NUM_TARGETS, 2))
        
        for position in target_positions:
            self.targets.append(Target(position))
    
    def check_collisions(self, puck):
        """Check for collisions between puck and targets"""
        newly_hit_targets = []
        for target in self.targets:
            if not target.hit and target.is_hit(puck):
                target.hit = True
                newly_hit_targets.append(target)
        return newly_hit_targets
    
    def all_targets_hit(self):
        """Check if all targets have been hit"""
        return all(target.hit for target in self.targets)
    
    def get_active_targets(self):
        """Get list of targets that haven't been hit"""
        return [target for target in self.targets if not target.hit] 