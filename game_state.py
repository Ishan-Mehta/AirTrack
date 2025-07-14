import time
from config import *

class GameState:
    def __init__(self):
        """Initialize game state"""
        self.score = 0
        self.start_time = time.time()
        self.game_duration = GAME_DURATION
        self.game_won_time = -1
        self.game_over = False
        self.victory = False
        
    def get_elapsed_time(self):
        """Get elapsed time since game start"""
        return round(time.time() - self.start_time, 2)
    
    def get_remaining_time(self):
        """Get remaining time in the game"""
        return self.game_duration - self.get_elapsed_time()
    
    def is_time_up(self):
        """Check if game time is up"""
        return self.get_elapsed_time() >= self.game_duration
    
    def add_score(self, points=1):
        """Add points to score"""
        self.score += points
    
    def check_game_end(self, all_targets_hit):
        """Check if game should end"""
        if self.game_over: 
            return
        if all_targets_hit:
            self.game_won_time = self.get_elapsed_time()
            self.victory = True
            self.game_over = True
        elif self.is_time_up():
            self.game_over = True