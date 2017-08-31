"""
Helper classes for hexagonal game of life implementations.
"""

import math as math


class GridHelper:
    def __init__(self, cell_radius, rows, cols, crop_bigger_grids):
        assert cell_radius > 0
        assert rows > 0
        assert cols > 0

        self.cell_radius = cell_radius
        self.row_size = rows
        self.col_size = cols
        self.crop = crop_bigger_grids

    def sanitize(self, grid):
        grid = self.sanitize_cols(grid)
        grid = self.sanitize_rows(grid)
        print(grid)
        return grid

    def sanitize_cols(self, grid):
        length = max([len(row) for row in grid])

        if length < self.col_size:
            return self.__expand_cols(grid, length)

        elif length > self.col_size and self.crop:
            return self.__crop_cols(grid, length)

        else:
            return GridHelper.__fill_grid(grid, length)

    def sanitize_rows(self, grid):
        if len(grid) < self.row_size:
            return self.__expand_rows(grid)

        elif len(grid) > self.row_size and self.crop:
            return self.__crop_rows(grid)

        else:
            return grid

    def __crop_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(max_length - self.col_size)
        right = max_length - right

        return [
            row[left:right]
            if len(row) > right
            else row + [False] * (right - len(row))
            for row in grid
        ]

    def __crop_rows(self, grid):
        start, end = GridHelper.__bisect(len(grid) - self.row_size)
        end = len(grid) - end
        return grid[start:end]

    def __expand_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(self.col_size - max_length)
        return [
            [False] * left
            + row
            + [False] * (right + max_length - len(row))
            for row in grid
        ]

    def __expand_rows(self, grid):
        row_length = len(grid[0])
        small, big = GridHelper.__bisect(self.row_size - len(grid))

        top = [[False] * row_length for _ in range(small)]
        bottom = [[False] * row_length for _ in range(big)]
        return top + grid + bottom

    @staticmethod
    def __bisect(number):
        small = number // 2
        big = number - small
        return small, big

    @staticmethod
    def __fill_grid(grid, max_length):
        return [
            row
            + [False] * (max_length - len(row))
            for row in grid]


class HexGeometry:
    @staticmethod
    def width(col_size, radius):
        return math.sqrt(3) * radius * (col_size + 1)

    @staticmethod
    def height(row_size, radius):
        size = 1.5 * radius * row_size
        border = (row_size % 2 + 1) / 4
        return size + border


class Illustrator:
    def __init__(self, cell_radius, row_size, col_size, palette=None):
        # Grid
        self.cell_radius = cell_radius
        self.row_size = row_size
        self.col_size = col_size

        # Visuals
        raw_width = HexGeometry.width(col_size, cell_radius)
        raw_height = HexGeometry.height(row_size, cell_radius)
        self.width, self.w_offset = Illustrator.__beautify(raw_width)
        self.height, self.h_offset = Illustrator.__beautify(raw_height)

        self.palette = palette

    def draw(self, generation):
        from PIL import Image

        img = Image.new("RGB", [self.width, self.height], (250, 0, 100))
        img.show()

    @staticmethod
    def __beautify(length):
        """Add minimum padding, than round up to next multiple of 40."""

        min_length = length + 10
        pretty_length = min_length + (- min_length % 40)
        offset = (pretty_length - length) // 2

        return int(pretty_length), int(offset)
