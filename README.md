# Space Invaders Game

A classic Space Invaders clone built with Pygame. This game features a player-controlled spaceship defending against waves of aliens, complete with shooting mechanics, health systems, and explosion animations.

## Features

- Player-controlled spaceship with health system
- Grid-based alien invasion force
- Shooting mechanics for both player and aliens
- Collision detection using sprite masks
- Explosion animations
- Health bar display
- Game state system (countdown, playing, win/lose conditions)
- Smooth sprite movements
- FPS-controlled game loop

## Prerequisites

To run this game, you'll need:

- Python 3.x
- Pygame library

## Installation

1. Clone this repository or download the source code
2. Install the required dependency:
```bash
pip install pygame
```

## Project Structure

The game requires the following file structure:

```
space-invaders/
│
├── main.py
└── img/
    ├── bg.png
    ├── spaceship.png
    ├── alien.png
    ├── bullet.png
    ├── alien_bullet.png
    └── exp1.png through exp5.png
```

## Controls

- **Arrow Keys**: Move the spaceship
  - Up/Down: Vertical movement (restricted to lower portion of screen)
  - Left/Right: Horizontal movement
- **Spacebar**: Shoot bullets
- **Close Window**: Exit game

## Game Mechanics

- Player starts with 3 health points
- Aliens move side to side in formation
- Random aliens will shoot at the player
- Player must avoid alien bullets while shooting down the aliens
- Game ends when either:
  - All aliens are destroyed (Victory)
  - Player health reaches zero (Game Over)

## Technical Details

### Constants
- Screen dimensions: 600x700 pixels
- FPS: 80
- Alien grid: 5x5
- Player speed: 5 pixels per frame
- Bullet speed: 5 pixels per frame (player), 2 pixels per frame (aliens)
- Maximum concurrent alien bullets: 5

### Classes

1. **Player**
   - Handles player movement
   - Manages health system
   - Controls shooting mechanics

2. **Invaders**
   - Controls alien movement patterns
   - Handles alien behavior

3. **Bullets**
   - Manages player projectiles
   - Handles collision detection

4. **Invader_Bullets**
   - Controls alien projectiles
   - Manages alien shooting mechanics

5. **Explosions**
   - Handles explosion animations
   - Supports multiple explosion sizes

## Contributing

Feel free to fork this project and submit pull requests with improvements. Some potential areas for enhancement:

- Add sound effects and background music
- Implement different types of aliens
- Add power-ups and special weapons
- Create multiple levels with increasing difficulty
- Add high score system

## License

This project is available under the MIT License. Feel free to use, modify, and distribute the code as you see fit.

## Credits

This game was created using Pygame and was inspired by the classic Space Invaders arcade game. All image assets should be properly credited to their respective creators.

## Troubleshooting

If you encounter any issues:

1. Ensure all required images are present in the `img` directory
2. Verify Pygame is properly installed
3. Check Python version compatibility
4. Ensure all image files match the expected filenames

For any additional issues, please open an issue in the repository.
