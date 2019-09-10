BOARD_SIZE = 9


def empty_board(size=BOARD_SIZE):
    return [[0 for _ in range(size)] for _ in range(size)]


def one_line_board(size=BOARD_SIZE):
    return [list(range(1, size+1))] + [[0 for _ in range(size)] for _ in range(size-1)]


EASY_BOARD = [[0, 0, 2, 0, 0, 0, 5, 0, 0],
              [0, 1, 0, 7, 0, 5, 0, 2, 0],
              [4, 0, 0, 0, 9, 0, 0, 0, 7],
              [0, 4, 9, 0, 0, 0, 7, 3, 0],
              [8, 0, 1, 0, 3, 0, 4, 0, 9],
              [0, 3, 6, 0, 0, 0, 2, 1, 0],
              [2, 0, 0, 0, 8, 0, 0, 0, 4],
              [0, 8, 0, 9, 0, 2, 0, 6, 0],
              [0, 0, 7, 0, 0, 0, 8, 0, 0]]

MEDIUM_BOARD = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 9, 0, 5, 0, 1, 8, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 7],
                [0, 0, 7, 3, 0, 6, 8, 0, 0],
                [4, 5, 0, 7, 0, 8, 0, 9, 6],
                [0, 0, 3, 5, 0, 2, 7, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 5],
                [0, 1, 6, 0, 3, 0, 4, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

HARD_BOARD = [[0, 0, 0, 0, 0, 3, 0, 1, 7],
              [0, 1, 5, 0, 0, 9, 0, 0, 8],
              [0, 6, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 7, 0, 0, 0],
              [0, 0, 9, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 5, 0, 0, 0, 0, 4],
              [0, 0, 0, 0, 0, 0, 0, 2, 0],
              [5, 0, 0, 6, 0, 0, 3, 4, 0],
              [3, 4, 0, 2, 0, 0, 0, 0, 0]]
