"""
Simple launcher for the Air Hockey Game
"""

from air_hockey_game import AirHockeyGame

def main():
    """Launch the air hockey game"""
    try:
        game = AirHockeyGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error running game: {e}")

if __name__ == "__main__":
    main() 