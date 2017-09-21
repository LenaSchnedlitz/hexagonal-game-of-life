<p align="center">
  <img src="https://github.com/Mailea/hexagonal-game-of-life/blob/master/logo.png"/>
</p>


# Hexagonal Game of Life
Conway's Game of Life on a hexagonal grid.

## How to Use
### Requirements
This program requires **Python 3.6**. Other requirements can be installed via
```
pip install -r requirements.txt
```

### Configuration and Start
#### General Settings
General settings can be found in *game.py*. The following attributes are available:
* `RULE_CONFIGURATION`: Regulations for cell birth and death.
* `GRID_CONFIGURATION`: Cell radius, grid size and grid cropping
* `COLOR_CONFIGURATION`: Color palette settings
* `SPEED`: Transition speed of gif frames

#### Game  
To start a new game, you have to create a new instance of the `Game` class. You can use any 2d-array of booleans as a `seed`. If not specified otherwise, 100 ticks (= generation progressions) will be made.

### Output
Generated `.gif`-files are saved as *'game.gif'* in the main program folder.
