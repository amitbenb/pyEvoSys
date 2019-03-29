import numpy as np


class Sudoku:
    def __init__(self, board=None):
        if board is None:
            self.board = np.zeros((4, 4), int)
        else:
            self.board = np.array(board)
        self.size = len(self.board)

    def get_elements(self):
        board = self.board
        size = self.size
        rs = int(np.sqrt(size))  # Root of size
        elements = np.array([i for i in board] + [i for i in board.transpose()])
        square_elements = np.array(
            [[board[(i // rs) + (rs * (j // rs))][(i % rs) + (rs * (j % rs))]
              for i in range(size)]
             for j in range(size)])
        elements = np.vstack((elements, square_elements))
        return elements

    def evaluate_board(self):
        ret_val = {'mistake_count': 0, 'bad_elements': 0}
        elements = self.get_elements()
        size = self.size
        for e in elements:
            number_of_duplicates = size - len(set(e).intersection(set(range(1, size+1))))
            ret_val['mistake_count'] += number_of_duplicates
            if number_of_duplicates > 0:
                ret_val['bad_elements'] += 1
        return ret_val

    def __str__(self):
        return 'Sudoku(' + '\n' + str(self.board) + ')'


if __name__ == "__main__":
    _board = np.array(np.random.permutation((np.arange(1, 17) % 4) + 1)).reshape(4, 4)
    # _board = np.array(list(range(1, 82))).reshape(9, 9)
    print(_board)
    print()
    _s = Sudoku(_board)
    print(_s)
    # print()
    # print(s.get_elements())
    # print()
    # print(s.evaluate_board())

