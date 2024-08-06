# Racer

A thrilling racing game built using Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Game Mechanics](#game-mechanics)
- [License](#license)

## Introduction

Racer is an exciting 2D racing game where players navigate a car to avoid obstacles and collect power-ups. The game gets progressively challenging as the speed of obstacles increases with each level.

## Features

- Simple and intuitive controls
- Increasing difficulty with each level
- Brake and power-up mechanics
- Sound effects for various actions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sayhan1610/racer.git
   cd racer
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the required assets:
   - Place your car images (`racer.png`, `car_red.png`, `car_blue.png`, `car_green.png`) in the `images` folder.
   - Place your audio files (`brake.mp3`, `car.mp3`, `crash.mp3`, `power.mp3`) in the `audio` folder.

## Usage

To start the game, run the following command:

```bash
python racer.py
```

## Controls

- **Arrow Keys**: Move the car left, right, up, and down
- **Spacebar**: Brake (with a cooldown period)
- **M**: Mute/Unmute sounds
- **P**: Pause/Unpause the game
- **Enter**: Start/Restart the game, Resume from pause, or Return to the main menu from the instructions

## Game Mechanics

- **Obstacles**: Avoid hitting the obstacles. The number and speed of obstacles increase with each level.
- **Power-ups**: Collect power-ups to gain temporary invincibility.
- **Levels**: The game becomes progressively harder as the player's level increases. Each level introduces faster obstacles.
- **Brake**: Use the brake to slow down obstacles temporarily. The brake has a cooldown period of 15 seconds.

## License

This project is licensed under the MIT License.
