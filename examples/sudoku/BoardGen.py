import random as r
import copy as cp
import numpy as np

import evo_core.Evolution as Evolution
import evo_core.evo_tools.Individuals as Individuals

import examples.sudoku.Sudoku as Sudoku
import examples.sudoku.SudokuConstants as SudConsts

# import examples.sudoku.EvoParams as EPs

DEBUG_OUTPUT = True


class BoardGenIndividual(Individuals.IntVectorIndividual):
    def __init__(self, genome, size, constraints=None):
        self.size = size
        self.constraints = constraints
        self.evaluated = None
        self.fitness = 0.0
        super(BoardGenIndividual, self).__init__(genome, min_int=1, max_int=size)
        self.sudoku = Sudoku.Sudoku(self.phenome)

    def develop(self):
        """

        :return: The phenotype for the Suduku
        """
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
        self.evaluated = self.sudoku.evaluate_board()
        self.fitness = 100.0 * (1 / (self.evaluated['mistake_count'] + 1))
        return self.fitness

    def get_fitness(self):
        return self.fitness

    def __str__(self):
        return '\n' + str(self.phenome)


class PopulationInitPhase(Evolution.EvoPhase):
    def __init__(self, ind_list, constraints=None, size=SudConsts.BOARD_SIZE):
        self.ind_list = ind_list
        self.pop_size = len(ind_list)
        self.constraints = constraints
        self.size = size

    def run(self, population):
        # print([i for i in self.ind_list if i is None])
        for idx, _ in enumerate(self.ind_list):
            self.ind_list[idx] = BoardGenIndividual(
                genome=generate_genome_for_constraints(self.size, constraints=self.constraints),
                constraints=self.constraints, size=self.size)

        # print([i for i in self.ind_list if i is None])
        # input()
        population.update_pop(self.ind_list)
        return population


class SwapMutationPhase(Evolution.EvoPhase):
    def __init__(self, probability=1.0):
        self.prob = probability

    def run(self, population):
        prob = self.prob
        for ind in population:
            if r.random() < prob:
                size = ind.size
                constraints = ind.constraints
                while True:  # Find a legal swap.
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

    def __repr__(self):
        return "Sudoku SwapMutationPhase prob=%.3f" % self.prob


class SwapsMutationPhase(Evolution.EvoPhase):
    def __init__(self, probability=1.0):
        self.prob = probability

    def run(self, population):
        prob = self.prob
        for ind in population:
            if r.random() < prob:
                while True:  # Find a legal swap.
                    size = ind.size
                    constraints = ind.constraints

                    while True:  # Allows multiple swaps
                        row = r.choice(range(size))
                        cols = r.sample(range(size), 2)
                        if constraints is None or (constraints[row][cols[0]] == 0 and constraints[row][cols[1]] == 0):
                            ind.rewrite_multiple_genes([size * row + cols[0], size * row + cols[1]],
                                                       [ind.genome[size * row + cols[1]],
                                                        ind.genome[size * row + cols[0]]])
                            break

                    if r.random() < 0.5:
                        # Prob 0.5 for a single swap, 0.25 for two swaps, 0.125 three swaps, etc.
                        break

        return population

    def __repr__(self):
        return "Sudoku SwapsMutationPhase prob=%.3f" % self.prob


class GreedySwapMutationPhase(Evolution.EvoPhase):
    def __init__(self, width=1, depth=1, probability=1.0):
        self.prob = probability
        self.width = width
        self.depth = depth

    def run(self, population):
        prob = self.prob
        for ind in population:
            if r.random() < prob:
                ind.calculate_fitness()
                self.mutate(ind)

        return population

    def __repr__(self):
        return "Sudoku GreedySwapMutationPhase prob=%.3f width=%d depth=%d" % (self.prob, self.width, self.depth)

    def mutate(self, ind):
        size = ind.size
        constraints = ind.constraints
        mistakes = ind.evaluated['mistake_count']
        mutation_successful = False
        for j in range(self.depth):
            for i in range(self.width):
                mutation_successful = False
                while True:
                    row = r.choice(range(size))
                    cols = r.sample(range(size), 2)
                    if constraints is None or (constraints[row][cols[0]] == 0 and constraints[row][cols[1]] == 0):
                        ind.rewrite_multiple_genes([size * row + cols[0], size * row + cols[1]],
                                                   [ind.genome[size * row + cols[1]], ind.genome[size * row + cols[0]]])
                        break
                ind.calculate_fitness()
                if ind.evaluated['mistake_count'] < mistakes:
                    mutation_successful = True
                    mistakes = ind.evaluated['mistake_count']
                else:
                    # Undo mutation
                    ind.rewrite_multiple_genes([size * row + cols[0], size * row + cols[1]],
                                               [ind.genome[size * row + cols[1]], ind.genome[size * row + cols[0]]])
                if mutation_successful:
                    break

            if mutation_successful:
                pass  # just let the inner loop try another mutation if depth is not exauhsted
            else:
                break  # Only keep mutating if you did well last time.


class GreedyPopulationCrossoverPhase(Evolution.EvoPhase):
    def __init__(self, probability=1.0, batch_size=2):
        self.probability = min(1.0, max(probability, 0.0))
        self.batch_size = batch_size

    def run(self, population):

        prob = self.probability
        new_pop = [None for _ in population]
        for idx, ind in enumerate(population):
            if r.random() < prob:
                s = Sudoku.Sudoku(ind.constraints if ind.constraints is not None else SudConsts.empty_board(ind.size))
                row_order = np.random.permutation(ind.size)
                # ind keeps line of index row_order[0]
                # s.board[row_order[0]] = cp.deepcopy(ind.phenome[row_order[0]])
                # for line_idx in row_order[1:]:
                #     self.add_best_row(population, line_idx, s)
                for row_idx in row_order:
                    self.add_best_row(population, row_idx, s)

                new_pop[idx] = BoardGenIndividual(s.board.flatten(), s.size, population[idx].constraints)

            else:
                new_pop[idx] = population[idx]

        population.update_pop(new_pop)

        return population

    def add_best_row(self, population, row_idx, board):
        """

        :param population:
        :param row_idx:
        :param board: Sudoku Board (type Sudoku.Sudoku)
        :return:
        """
        # ind_order = np.random.permutation(len(population))
        ind_order = np.random.permutation(len(population))[:self.batch_size]
        curr_row = population[ind_order[0]].sudoku.board[row_idx]
        curr_constraints_penalty = self.add_row_constraints_penalty(curr_row, board, row_idx)
        for ind_idx in ind_order[1:]:
            candidate_row = population[ind_idx].sudoku.board[row_idx]
            candidate_row_penalty = self.add_row_constraints_penalty(curr_row, board, row_idx)
            if curr_constraints_penalty > candidate_row_penalty:
                curr_row = candidate_row
                curr_constraints_penalty = candidate_row_penalty

        board.board[row_idx] = cp.deepcopy(curr_row)

    @staticmethod
    def add_row_constraints_penalty(curr_row, board, row_idx):
        """

        :param curr_row:
        :param board: Sudoku Board (type Sudoku.Sudoku)
        :param row_idx:
        :return: Number of constraints broken by adding row.
        """
        old_row = cp.deepcopy(board.board[row_idx])  # Backup
        # print(old_row)
        # print(curr_row)
        board.board[row_idx] = cp.deepcopy(curr_row)  # try out the new row.
        # print(old_row)
        # print(curr_row)
        # input()

        ret_val = board.evaluate_board()['mistake_count']

        board.board[row_idx] = old_row  # Revert to original

        return ret_val

    def __repr__(self):
        return "Sudoku GreedyPopulationCrossoverPhase prob=%.3f batch_size=%d" % (self.probability, self.batch_size)


class FitnessEvaluationPhase(Evolution.EvoPhase):
    def run(self, population):
        for ind in population:
            ind.calculate_fitness()

        return population

    def __repr__(self):
        return "Sudoku FitnessEvaluationPhase"


class SaveSolutionsPhase(Evolution.EvoPhase):
    def __init__(self,):
        self.solutions = []
        self.solution_hashes = []

    def restart(self):
        self.solutions = []
        self.solution_hashes = []

    def run(self, population):
        for ind in population:
            if ind.get_fitness() == 100.0:
                hash_value = hash(str(ind.phenome))
                # print(hash_value)
                if hash_value not in self.solution_hashes:
                    # print(len(self.solutions))
                    self.solution_hashes.append(hash_value)
                    self.solutions.append(cp.deepcopy(ind.phenome))
                    # print(len(self.solutions))

        return population

    def __repr__(self):
        return "Sudoku FitnessEvaluationPhase"


class FitnessDistorterPhase(Evolution.EvoPhase):
    def __init__(self, solutions_phase, solution_grace_period):
        """
        :param solutions_phase: the SaveSolutionsPhase phase that contains solutions already found
        :param solution_grace_period: once every solution_grace_period
                                      the list of forbidden solution hashes is updated.
        """
        self.solutions_phase = solutions_phase
        self.forbidden_hashes = []
        self.solution_grace_period = solution_grace_period
        self.gen_counter = 0

    def run(self, population):
        self.gen_counter += 1
        if self.gen_counter >= self.solution_grace_period:
            self.gen_counter = 0
            self.forbidden_hashes = cp.deepcopy(self.solutions_phase.solution_hashes)
        for ind in population:
            if ind.get_fitness() == 100.0:
                hash_value = hash(str(ind.phenome))
                if hash_value in self.forbidden_hashes:
                    ind.fitness = 0.0
        return population

    def __repr__(self):
        return "Sudoku FitnessDistorterPhase grace_period=%d generations" % self.solution_grace_period


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

