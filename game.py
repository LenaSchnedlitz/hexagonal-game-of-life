"""
A variant of Conway's Game of Life on a hexagonal grid.

Rules: B2/S12
 - Dead cells with two live neighbours are born.
 - Live cells with one or two live neighbours survive.
 - All other live cells die.

"""
import helper as helper

RULE_CONFIGURATION = {
    'b': (2,),  # Birth
    's': (1, 2)  # Survival
}

GRID_CONFIGURATION = {
    'cell_radius': 6,
    'rows': 37,
    'cols': 43,
    'crop_bigger_grids': True
}

GRID_CONFIGURATION['rows'] = 5
GRID_CONFIGURATION['cols'] = 3


class Game:
    def __init__(self, seed, max_steps=0):
        self.helper = helper.GridHelper(**GRID_CONFIGURATION)
        seed = self.helper.sanitize(seed)
        self.generation = Generation(seed)
        self.illustrator = Game.__set_up_illustrator(seed)
        self.max = max_steps
        self.count = 0

    def play(self):
        self.illustrator.draw(self.generation)

        while self.count < self.max:
            self.generation = self.generation.tick()
            self.illustrator.draw(self.generation)
            self.count += 1

    @staticmethod
    def __set_up_illustrator(seed):
        config = {
            'cell_radius': GRID_CONFIGURATION.get('cell_radius'),
            'row_count': len(seed),
            'col_count': len(seed[0])
        }
        return helper.Illustrator(**config)


class Generation:
    def __init__(self, grid, previous=None):
        self._grid = grid
        self._previous = previous
        self._rows = len(self._grid)
        self._cols = len(self._grid[0])

    def tick(self):
        new_grid = [
            [
                (
                    self._is_born((row_index, col_index))
                    or self._survives((row_index, col_index))
                )
                for col_index, col in enumerate(row)
            ]
            for row_index, row in enumerate(self._grid)
        ]
        return Generation(new_grid, self)

    def is_alive(self, cell):
        row, col = cell
        return self._grid[row % self._rows][col % self._cols]

    def was_alive(self, cell):
        if self._previous:
            return self._previous.is_alive(cell)
        else:
            return self.is_alive(cell)

    def _is_born(self, cell):
        return not self.is_alive(cell) \
               and sum(self._neighbours(cell)) in RULE_CONFIGURATION.get('b')

    def _survives(self, cell):
        return self.is_alive(cell) \
               and sum(self._neighbours(cell)) in RULE_CONFIGURATION.get('s')

    def _neighbours(self, cell):
        row, col = cell
        positions = Generation._relative_neighbour_coordinates(row % 2)

        neighbours = [
            self._grid[(row + r) % self._rows][(col + c) % self._cols]
            for (r, c) in positions
        ]
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
