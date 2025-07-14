import numpy as np
import time
from config import *

class PhysicsEngine:
    def __init__(self):
        """Initialize physics engine"""
        self.previous_collision_time = -1
    
    def check_wall_collision(self, puck):
        """Check for collisions with walls and handle bouncing"""
        # Check left and right walls
        if puck.position[0] <= puck.radius + 1:                 # Left wall
            puck.position[0] = puck.radius + 1                  # +1 just in case
            puck.velocity[0] = -puck.velocity[0]
        elif puck.position[0] + puck.radius >= VIDEO_X - 1:     # Right wall
            puck.position[0] = VIDEO_X - puck.radius - 1        # -1 just in case
            puck.velocity[0] = -puck.velocity[0]
        
        # Check top and bottom walls
        if puck.position[1] <= puck.radius + 1:                 # Top wall
            puck.position[1] = puck.radius + 1
            puck.velocity[1] = -puck.velocity[1]
        elif puck.position[1] + puck.radius >= VIDEO_Y - 1:     # Bottom wall
            puck.position[1] = VIDEO_Y - puck.radius - 1
            puck.velocity[1] = -puck.velocity[1]
    
    def check_paddle_collision(self, puck, paddle, current_time):
        """Check for collision between puck and paddle"""
        dx = puck.position[0] - paddle.position[0]
        dy = puck.position[1] - paddle.position[1]
        distance = np.sqrt(dx ** 2 + dy ** 2)
        # distance = np.linalg.norm(puck.position - np.array(paddle.position))

        if distance <= (puck.radius + paddle.radius + 1) and self.previous_collision_time + 0.5 < current_time:
            # Get the angle in cos and sin terms for the collision normal vector
            collision_normal = np.array([dx / distance, dy / distance])
        
            # Get current velocity as numpy array
            current_velocity = np.array(puck.velocity)
            
            # Calculate velocity components
            # Parallel component (along collision normal) (vel vector . dir vector = parallel vel vector)
            # This is: vx cos + vy sin
            parallel_vel = np.dot(current_velocity, collision_normal)
            
            # Perpendicular component (tangent to collision surface)
            # This is actually: vx sin^2 + vy cos^2
            perpendicular_vel_sq = current_velocity - parallel_vel * collision_normal
            
            # Reverse the parallel component (bounce)
            # This is actually: -vx cos^2 - vy sin^2
            new_parallel_vel_sq = -parallel_vel * collision_normal
            
            # Combine components for new velocity
            # This becomes: vx (sin^2 - cos^2) + vy (cos^2 - sin^2)
            new_velocity = perpendicular_vel_sq + new_parallel_vel_sq
            
            # Update puck velocity (keep as numpy array)
            puck.velocity = new_velocity.astype(float)
            
            # Move puck outside paddle to prevent sticking
            overlap = np.ceil((puck.radius + paddle.radius) - distance).astype(int)
            puck.position += collision_normal.astype(int) * (overlap + 2)

            self.previous_collision_time = current_time

            return True
        
        return False