"""
A variant of Conway's Game of Life on a hexagonal grid.

Rules: B2/S12
 - Dead cells with two live neighbours are born.
 - Live cells with one or two live neighbours survive.
 - All other live cells die.

"""

from operator import add

# Rule Configuration
B_RULE = (2,)  # Birth
S_RULE = (1, 2)  # Survival


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

    def _count(self, cells):
        return 0

    def _is_born(self, cell):
        return self._count(Generation._neighbours(cell)) in B_RULE

    def _survives(self, cell):
        return self._count(Generation._neighbours(cell)) in S_RULE

    @staticmethod
    def _neighbours(cell):
        row, _ = cell

        left = - (row % 2)
        right = left + 1
        relative_neighbour_coordinates = (
            (-1, left), (-1, right),
            (0, -1), (0, 1),
            (1, left), (1, right)
        )

        return map(add, cell, relative_neighbour_coordinates)
