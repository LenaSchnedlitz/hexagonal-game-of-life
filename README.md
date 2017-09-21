<p align="center">
  <img src="https://github.com/Mailea/hexagonal-game-of-life/blob/master/logo.png"/>
</p>


# Hexagonal Game of Life
Conway's Game of Life on a hexagonal grid.

## How to Use
### Requirements
This program requires **Python 3.6**.  
All other requirements are listed in *requirements.txt* and can be installed with Pip:
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
A new game can be started by calling the `play()`-Method of a `Game` instance.  

The `Game` constructor takes up to two parameters:
* `seed`: a 2 dimensional boolean array
* `ticks`: number of produced generations

Executing *game.py* will start a default game.

### Output
Generated *.gif*-files are saved as *'game.gif'* in the main program folder.
