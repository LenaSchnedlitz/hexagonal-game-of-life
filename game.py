"""
A variant of Conway's Game of Life on a hexagonal grid.

Rules: B2/S12
 - Dead cells with two live neighbours are born.
 - Live cells with one or two live neighbours survive.
 - All other live cells die.

"""

# Rule Configuration
STATES = ('DEAD', 'ALIVE')
B = (2,)
S = (1, 2)


class Game:
    def __init__(self, seed, max_steps=100):
        self.generation = seed
        self.max = max_steps
        self.count = 0

    def play(self):
        self.generation.draw()

        while self.count < self.max:
            self.generation = self.generation.tick()
            self.generation.draw()
            self.count += 1


class Generation:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def draw(self):
        # TODO
        pass

    def tick(self):
        # TODO
        pass

    def _survives(self, row, col):
        # TODO
        pass

    def _is_born(self, row, col):
        # TODO
        pass
