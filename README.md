# AirTrack: Vision-Controlled Single-Player Air Hockey Game

A finger-tracking air hockey game built with OpenCV and MediaPipe. Control a paddle with your index finger to hit targets with a puck!

## Features

- **Finger Tracking**: Use your index finger to control the paddle
- **Physics Engine**: Realistic puck movement and collision detection
- **Target System**: Hit targets to score points and increase difficulty (feature to add)
- **Timer**: Race against time to hit all targets
- **Score Tracking**: Keep track of your performance

## Project Structure

The project has been restructured into modular components for better organization:

```
AirTrack/
├── config.py              # Game configuration and constants
├── camera.py              # Camera handling and frame processing
├── hand_tracker.py        # MediaPipe hand tracking
├── game_objects.py        # Game objects (Puck, Paddle, Targets)
├── renderer.py            # Drawing and rendering functions
├── physics.py             # Physics engine and collision detection
├── game_state.py          # Game state management
├── air_hockey_game.py     # Main game class
├── run_game.py            # Simple launcher script
├── target.png             # Target image
└── requirements.txt       # Python dependencies
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure you have a webcam connected** (the game uses camera index 0 by default)

## How to Play

### Running the Game

**Option 1: Using the launcher script**
```bash
python run_game.py
```

**Option 2: Direct execution**
```bash
python air_hockey_game.py
```

### Game Controls

- **Index Finger**: Control the paddle position
- **'q' key**: Quit the game
- **Time Limit**: 30 seconds to hit all targets

### Gameplay

1. **Objective**: Hit all the targets with the puck before time runs out
2. **Paddle Control**: Move your index finger in front of the camera to control the green paddle
3. **Physics**: The blue puck bounces off walls and your paddle
4. **Scoring**: Each target hit gives you 1 point and increases puck speed
5. **Victory**: Hit all targets to win!
6. **Defeat**: Run out of time and lose

## Configuration

You can modify game settings in `config.py`: (some of them mentioned below)

- `VIDEO_X, VIDEO_Y`: Camera resolution
- `GAME_DURATION`: Game time limit in seconds
- `TARGET_SIZE`: Size of target images
- `NUM_TARGETS`: Number of targets to hit
- `PUCK_RADIUS, PADDLE_RADIUS`: Object sizes
- `INITIAL_PUCK_VELOCITY`: Starting puck speed

## Technical Details

### Architecture

The game follows a modular design pattern:

- **Separation of Concerns**: Each module handles a specific aspect of the game
- **Object-Oriented Design**: Classes for game objects and systems
- **Configuration Management**: Centralized settings in `config.py`
- **Error Handling**: Graceful handling of camera and tracking errors

### Key Components

1. **HandTracker**: Manages MediaPipe hand detection and finger tracking
2. **PhysicsEngine**: Handles collision detection and physics calculations
3. **Renderer**: Manages all drawing and overlay operations
4. **GameState**: Tracks score, time, and game progression
5. **TargetManager**: Manages target positions and collision detection

### Dependencies

- `opencv-python`: Computer vision and camera handling
- `mediapipe`: Hand tracking and landmark detection
- `numpy`: Numerical operations and array handling

## Troubleshooting

### Common Issues

1. **Camera not found**: Ensure your webcam is connected and not in use by another application
2. **Hand tracking issues**: Ensure good lighting and keep your hand clearly visible
3. **Performance issues**: Lower the camera resolution in `config.py` if needed

### Performance Tips

- Ensure good lighting for better hand tracking
- Keep your hand within the camera frame, but at a shoulder distance from the camera for best experience
- Close other applications using the camera

## Contributing

Feel free to improve the game by:
- Adding new features
   - Tracking the paddle's velocity to use it as a parameter during collion
- Optimizing performance
- Testing bugs and reporting
- Improving the physics engine 
   - The collision between the puck and the paddle has margin to improve
- Enhancing the UI/UX
