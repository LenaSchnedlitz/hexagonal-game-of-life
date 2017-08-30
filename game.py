"""
A variant of Conway's Game of Life on a hexagonal grid.

Rules: B2/S12
 - Dead cells with two live neighbours are born.
 - Live cells with one or two live neighbours survive.
 - All other live cells die.

"""
from helper import GridHelper


RULE_CONFIGURATION = {
    'B': (2,),  # Birth
    'S': (1, 2)  # Survival
}

GRID_CONFIGURATION = {
    'CELL_RADIUS': 6,
    'ROWS': 35,
    'COLS': 42,
    'CROP_BIGGER_GRIDS': True
}


class Game:
    def __init__(self, seed, max_steps=100):
        self.helper = GridHelper(GRID_CONFIGURATION)
        self.generation = Generation(self.helper.sanitize(seed))
        self.max = max_steps
        self.count = 0

    def play(self):
        self.generation.draw()

        while self.count < self.max:
            self.generation = self.generation.tick()
            self.generation.draw()
            self.count += 1


class Generation:
    def __init__(self, grid):
        self._grid = grid
        self._rows = len(self._grid)
        self._cols = len(self._grid[0])

    def draw(self):
        # TODO
        pass

    def tick(self):
        new_grid = [[
            (self._is_born((row_i, col_i)) or self._survives((row_i, col_i)))
            for col_i, col in enumerate(row)]
            for row_i, row in enumerate(self._grid)]
        return Generation(new_grid)

    def is_alive(self, cell):
        row, col = cell
        return self._grid[row][col]

    def _is_born(self, cell):
        return not self.is_alive(cell) \
               and sum(self._neighbours(cell)) in RULE_CONFIGURATION.get('B')

    def _survives(self, cell):
        return self.is_alive(cell) \
               and sum(self._neighbours(cell)) in RULE_CONFIGURATION.get('S')

    def _neighbours(self, cell):
        row, col = cell
        positions = self._relative_neighbour_coordinates(row % 2)

        neighbours = [
            self._grid[(row + r) % self._rows][(col + c) % self._cols]
            for (r, c) in positions]
        return neighbours

    @staticmethod
    def _relative_neighbour_coordinates(offset):
        # offset is caused by alternating cell alignment in a hex grid

        left, right = -offset, -offset + 1
        return (
            (-1, left), (-1, right),
            (0, -1), (0, 1),
            (1, left), (1, right)
        )


test_seed = [
    [False, False, False, True],
    [False, False, True, False],
    [False, True, False, True],
    [True, True, False, True]
]

Game(test_seed).play()
