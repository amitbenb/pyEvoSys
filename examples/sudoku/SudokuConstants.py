BOARD_SIZE = 16


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

