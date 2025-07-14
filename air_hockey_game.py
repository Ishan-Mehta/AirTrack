import cv2
import time
from config import *
from camera import Camera
import game_state
from hand_tracker import HandTracker
from game_objects import Puck, Paddle, TargetManager
from renderer import Renderer
from physics import PhysicsEngine
from game_state import GameState

class AirHockeyGame:
    def __init__(self):
        """Initialize the air hockey game"""
        self.camera = Camera()
        self.hand_tracker = HandTracker()
        self.puck = Puck()
        self.paddle = Paddle()
        self.target_manager = TargetManager()
        self.renderer = Renderer()
        self.physics = PhysicsEngine()
        self.game_state = GameState()
        
    def run(self):
        """Main game loop"""
        # Error handling for camera
        if not self.camera.cap.isOpened():
            print("Error: Could not open camera")
            return
            
        # Print game instructions on the terminal
        print("Air Hockey Game Started!")
        print("Use your index finger to control the paddle")
        print("Press 'q' to quit")
        
        while True:
            # Read camera frame (& flip it for selfie view)
            frame, success = self.camera.read_frame()
            if not success:
                print('Ignoring empty camera frame')
                break
            
            # Convert to RGB for processing (OpenCV uses BGR)
            image = self.camera.convert_to_rgb(frame)
            
            # Process hand tracking
            results = self.hand_tracker.process_frame(image)
            
            # FEATURE TO ADD:
            # There should be a tracking of paddle's velocity.
            # The paddle's velocity can be accounted in collision with the puck
            # Update paddle position
            paddle_position = self.hand_tracker.get_paddle_position(results)
            if paddle_position:
                self.paddle.update_position(paddle_position)
            
            # Update puck position
            current_time = time.time()
            self.puck.update_position()
            
            self.physics.check_wall_collision(self.puck)
            # NEEDS TO BE FIXED:
            # Does not work perfectly for collisions with very small collision normal 
            # i.e. (collision normal almost perpendicular to velocity)
            # Does not work when the paddle crosses the puck in its direction.
            self.physics.check_paddle_collision(self.puck, self.paddle, current_time)
            
            # Check target collisions
            newly_hit_targets = self.target_manager.check_collisions(self.puck)
            for target in newly_hit_targets:
                self.game_state.add_score()
                # NEEDS TO BE TESTED --- Might not work properly in this context
                self.puck.increase_velocity()
            
            # Check game end conditions
            self.game_state.check_game_end(self.target_manager.all_targets_hit())
            
            # Render everything
            self.renderer.overlay_targets(image, self.target_manager.targets)
            self.renderer.overlay_circle(image, self.puck.position, self.puck.radius, PUCK_COLOR)
            self.renderer.overlay_circle(image, self.paddle.position, self.paddle.radius, PADDLE_COLOR)
            
            # Draw UI
            self.renderer.draw_ui(image, self.game_state.score, self.game_state.get_remaining_time(), self.game_state.game_over)
            
            # Handle game over
            if self.game_state.game_over:
                if self.game_state.victory:
                    self.renderer.draw_victory(image, self.game_state.score, self.game_state.game_won_time)
                else:
                    self.renderer.draw_game_over(image, self.game_state.score)
                
                # Display final screen for a few seconds
                display_image = self.camera.convert_to_bgr(image)
                cv2.imshow('Virtual Air Hockey', display_image)
                
                if self.game_state.get_elapsed_time() > self.game_state.game_duration + 10:
                    break
            else:
                # Display normal game frame (Convert from RGB to BGR for OpenCV)
                display_image = self.camera.convert_to_bgr(image)
                cv2.imshow('Virtual Air Hockey', display_image)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.camera.cap.release()
        cv2.destroyAllWindows()
        print("Game ended!")

if __name__ == "__main__":
    game = AirHockeyGame()
    game.run() 