"""
Helper classes for game of life implementations.
"""


class GridHelper:
    def __init__(self, config):
        self.rows = config.get('ROWS')
        self.cols = config.get('COLS')
        self.crop = config.get('CROP_BIGGER_GRIDS')

    def sanitize(self, grid):
        grid = self.sanitize_cols(grid)
        print(grid)
        grid = self.sanitize_rows(grid)
        return grid

    def sanitize_cols(self, grid):
        length = max([len(row) for row in grid])

        if length < self.cols:
            return self.__expand_cols(grid, length)

        elif length > self.cols and self.crop:
            return self.__crop_cols(grid, length)

        else:
            return GridHelper.__fill_grid(grid, length)

    def sanitize_rows(self, grid):
        if len(grid) < self.rows:
            return self.__expand_rows(grid)

        elif len(grid) > self.rows and self.crop:
            return self.__crop_rows(grid)

        else:
            return grid

    def __crop_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(max_length - self.cols)
        right = max_length - right

        return [
            row[left:right]
            if len(row) > right
            else row + [False] * (right - len(row))
            for row in grid
        ]

    def __crop_rows(self, grid):
        start, end = GridHelper.__bisect(len(grid) - self.rows)
        end = len(grid) - end
        return grid[start:end]

    def __expand_cols(self, grid, max_length):
        left, right = GridHelper.__bisect(self.cols - max_length)
        return [
            [False] * left
            + row
            + [False] * (right + max_length - len(row))
            for row in grid
        ]

    def __expand_rows(self, grid):
        row_length = len(grid[0])
        small, big = GridHelper.__bisect(self.rows - len(grid))

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
