import evo_core.Population_Containers as PopContainers
import evo_core.Evolution as Evolution
import examples.sudoku.SudokuConstants

from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.SudokuConstants as Consts

num_of_generations = 1000
pop_size = 2000
mut_prob = 0.8
tour_size = 4

get_fitness = BoardGen.BoardGenIndividual.get_fitness
calculate_fitness = BoardGen.BoardGenIndividual.calculate_fitness

init_p = MiscPhases.SimpleInitPhase(num_of_generations)
size = examples.sudoku.SudokuConstants.BOARD_SIZE
# constraints = None
# constraints = Consts.EASY_BOARD
constraints = Consts.one_line_board()
# print(np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size))))
# input()
# inds = [BoardGen.BoardGenIndividual(
#     genome=np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size))),
#     size=size)
#     for _ in range(pop_size)]
inds = [BoardGen.BoardGenIndividual(
    genome=BoardGen.generate_genome_for_constraints(size, constraints=constraints),
    constraints=constraints, size=size)
    for _ in range(pop_size)]

# pop = PopContainers.SimplePopulation()
pop = PopContainers.SimplePopulationWithElite()
pop.update_pop(inds)

init_p = MiscPhases.SimpleInitPhase(num_of_generations)
select_p = Selection.TournamentSelectionPhase(get_fitness, tour_size=tour_size)
mut_p = BoardGen.SwapMutationPhase(probability=mut_prob)
eval_p = BoardGen.FitnessEvaluationPhase()
elite_e_p = Selection.SimpleExtractElitePhase(get_fitness, elite_size=tour_size)
elite_m_p = Selection.SimpleMergeElitePhase()
# cyc = Evolution.Cycle([select_p, mut_p, eval_p, record_p])
