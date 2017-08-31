"""
Helper classes for hexagonal game of life implementations.
"""

import math as math

from PIL import Image, ImageDraw


class GridHelper:
    def __init__(self, cell_radius, rows, cols, crop_bigger_grids):
        assert cell_radius > 0
        assert rows > 0
        assert cols > 0

        self.cell_radius = cell_radius
        self.row_count = rows
        self.col_count = cols
        self.crop = crop_bigger_grids

    def sanitize(self, grid):
        grid = self.sanitize_cols(grid)
        grid = self.sanitize_rows(grid)
        return grid

    def sanitize_cols(self, grid):
        length = max([len(row) for row in grid])

        if length < self.col_count:
            return self.__expand_cols(grid, length)

        elif length > self.col_count and self.crop:
            return self.__crop_cols(grid, length)

        else:
            return GridHelper.__fill_grid(grid, length)

    def sanitize_rows(self, grid):
        if len(grid) < self.row_count:
            return self.__expand_rows(grid)

        elif len(grid) > self.row_count and self.crop:
            return self.__crop_rows(grid)

        else:
            return grid

    def __crop_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(max_length - self.col_count)
        right = max_length - right

        return [
            row[left:right]
            if len(row) > right
            else row + [False] * (right - len(row))
            for row in grid
        ]

    def __crop_rows(self, grid):
        start, end = GridHelper.__bisect(len(grid) - self.row_count)
        end = len(grid) - end
        return grid[start:end]

    def __expand_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(self.col_count - max_length)
        return [
            [False] * left
            + row
            + [False] * (right + max_length - len(row))
            for row in grid
        ]

    def __expand_rows(self, grid):
        row_length = len(grid[0])
        small, big = GridHelper.__bisect(self.row_count - len(grid))

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
    def hexagon(row, col, radius, w_offset, h_offset):
        root = math.sqrt(3)
        hexagon = [
            (0, 0),
            (0, radius),
            (0.5 * root * radius, 1.5 * radius),
            (root * radius, radius),
            (root * radius, 0),
            (0.5 * root * radius, -0.5 * radius)
        ]
        odd_even_offset = -0.5 * (row % 2) * HexGeometry.cell_width(radius)
        r = row * HexGeometry.cell_height(radius) + h_offset
        c = col * HexGeometry.cell_width(radius) + w_offset + odd_even_offset

        return [(c + c_hex, r + r_hex) for (c_hex, r_hex) in hexagon]

    @staticmethod
    def cell_height(radius):
        return 1.5 * radius

    @staticmethod
    def cell_width(radius):
        return math.sqrt(3) * radius

    @staticmethod
    def height(row_size, radius):
        return HexGeometry.cell_height(radius) * row_size + 0.5 * radius

    @staticmethod
    def width(col_size, radius):
        return HexGeometry.cell_width(radius) * (col_size + 1)

    @staticmethod
    def width_offset(raw_offset, radius):
        return raw_offset + 0.5 * math.sqrt(3) * radius

    @staticmethod
    def height_offset(raw_offset, radius):
        return raw_offset + 0.5 * radius


class Illustrator:
    def __init__(self, cell_radius, row_count, col_count, palette=None):
        # Grid
        self.cell_radius = cell_radius
        self.row_count = row_count
        self.col_count = col_count

        # Image Coordinates
        raw_width = HexGeometry.width(col_count, cell_radius)
        raw_height = HexGeometry.height(row_count, cell_radius)
        self.width, raw_w_offset = self.__beautify(raw_width)
        self.height, raw_h_offset = self.__beautify(raw_height)
        self.w_offset = HexGeometry.width_offset(raw_w_offset, cell_radius)
        self.h_offset = HexGeometry.height_offset(raw_h_offset, cell_radius)

        # Color
        self.palette = palette

    def draw(self, generation):
        img = Image.new('RGB', [self.width, self.height], (250, 0, 100))
        draw = ImageDraw.Draw(img, 'RGB')
        params = {
            'radius': self.cell_radius,
            'w_offset': self.w_offset,
            'h_offset': self.h_offset
        }

        for row in range(self.row_count):
            for col in range(self.col_count + row % 2):
                color = (250, 0, 100)
                if generation.is_alive([row, col]):
                    color = (255, 255, 255)
                draw.polygon(HexGeometry.hexagon(row, col, **params),
                             fill=color, outline=color)
        img.show()

    def __beautify(self, length):
        """Add minimum padding, then round up to next multiple of n."""
        min_padding = HexGeometry.cell_width(self.cell_radius)
        n = 40

        min_length = length + min_padding
        pretty_length = min_length + (- min_length % n)
        offset = (pretty_length - length) / 2

        return int(pretty_length), offset
