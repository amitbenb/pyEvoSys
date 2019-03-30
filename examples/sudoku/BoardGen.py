import random as r
import copy as cp
import numpy as np

import evo_core.Evolution as Evolution
import evo_core.evo_tools.Individuals as Individuals

import examples.sudoku.Sudoku as Sudoku

DEBUG_OUTPUT = True


class BoardGenIndividual(Individuals.IntVectorIndividual):
    def __init__(self, genome, size, constraints=None):
        self.size = size
        self.constraints = constraints
        self.fitness = 0.0
        super(BoardGenIndividual, self).__init__(genome, min_int=1, max_int=size)
        self.sudoku = Sudoku.Sudoku(self.phenome)

    def develop(self):
        size = self.size
        board = np.zeros((size,  size), int).reshape(size, size)
        constraints = self.constraints
        for i in range(size):
            for j in range(size):
                board[i][j] = self.genome[i * size + j]
        # np.array([i[j] for j in i] for i in self.genome)
        if constraints is not None:
            for i in range(size):
                for j in range(size):
                    if constraints[i][j] != 0:
                        board[i][j] = constraints[i][j]

        return board

    def self_replicate(self):
        return cp.deepcopy(self)

    def calculate_fitness(self):
        self.phenome = self.develop()
        self.sudoku = Sudoku.Sudoku(self.phenome)
        self.fitness = 100.0 * (1 / (self.sudoku.evaluate_board()['mistake_count'] + 1))
        return self.fitness

    def get_fitness(self):
        return self.fitness

    def __str__(self):
        return '\n' + str(self.phenome)


class SwapMutationPhase(Evolution.EvoPhase):
    def __init__(self, probability=1.0):
        self.prob = probability

    def run(self, population):
        prob = self.prob
        for ind in population:
            if r.random() < prob:
                size = ind.size
                constraints = ind.constraints
                while True:
                    row = r.choice(range(size))
                    cols = r.sample(range(size), 2)
                    if constraints is None or (constraints[row][cols[0]] == 0 and constraints[row][cols[1]] == 0):
                        # if row == 0:
                        #     print(ind.genome[:16])
                        #     print(cols[0], cols[1])
                        #     print(constraints[row])
                        #     print("*****")
                        ind.rewrite_multiple_genes([size * row + cols[0], size * row + cols[1]],
                                                   [ind.genome[size * row + cols[1]], ind.genome[size * row + cols[0]]])
                        # if row == 0:
                        #     print(ind.genome[:16])
                        #     print("*****")
                        break

        return population


class FitnessEvaluationPhase(Evolution.EvoPhase):
    def run(self, population):
        for ind in population:
            ind.calculate_fitness()

        return population


def generate_genome_for_constraints(size, constraints=None):
    if constraints is None:
        return np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size)))
    else:
        ans = np.zeros((size, size), int)
        for i in range(size):
            permuted_row = np.random.permutation([j for j in range(1, size + 1) if j not in constraints[i]])
            k = 0
            for j in range(size):
                if constraints[i][j] != 0:
                    ans[i][j] = constraints[i][j]
                else:
                    ans[i][j] = permuted_row[k]
                    k += 1

        return np.concatenate([i for i in ans])


