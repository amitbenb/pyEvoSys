import evo_core.Population_Containers as PopContainers
import examples.sudoku.SudokuConstants

from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.SudokuConstants as Consts

num_of_generations = 200
pop_size = 200
mut_prob = 0.2
gmut_prob = 1.0
gmut_width = 10
gmut_depth = 10
tour_size = 2
tour_winners = 1
elite_size = 4

get_fitness = BoardGen.BoardGenIndividual.get_fitness
calculate_fitness = BoardGen.BoardGenIndividual.calculate_fitness

size = examples.sudoku.SudokuConstants.BOARD_SIZE
# constraints = None
constraints = Consts.EASY_BOARD
# constraints = Consts.HARD_BOARD
# constraints = Consts.one_line_board()

# inds = [BoardGen.BoardGenIndividual(
#     genome=np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size))),
#     size=size)
#     for _ in range(pop_size)]
# inds = [BoardGen.BoardGenIndividual(
#     genome=BoardGen.generate_genome_for_constraints(size, constraints=constraints),
#     constraints=constraints, size=size)
#     for _ in range(pop_size)]
inds = [None for _ in range(pop_size)]
pop_init_p = BoardGen.PopulationInitPhase(ind_list=inds, constraints=constraints)
init_p = MiscPhases.SimpleInitPhase(num_of_generations)

# pop = PopContainers.SimplePopulation()
pop = PopContainers.SimplePopulationWithElite()
# pop.update_pop(inds)

null_select_p = Selection.SimpleNullSelectionPhase()
select_p = Selection.TournamentSelectionPhase(get_fitness, tour_size=tour_size, tour_winners=tour_winners)
# mut_p = BoardGen.SwapMutationPhase(probability=mut_prob)
mut_p = BoardGen.SwapsMutationPhase(probability=mut_prob)
gmut_p = BoardGen.GreedySwapMutationPhase(probability=gmut_prob, width=gmut_width, depth=gmut_depth)
gxo_p = BoardGen.GreedyPopulationCrossoverPhase(probability=1.0, batch_size=4)
eval_p = BoardGen.FitnessEvaluationPhase()
elite_e_p = Selection.SimpleExtractElitePhase(get_fitness, elite_size=elite_size)
elite_m_p = Selection.SimpleMergeElitePhase()
save_solutions_p = BoardGen.SaveSolutionsPhase()
distorter_p = BoardGen.FitnessDistorterPhase(save_solutions_p, solution_grace_period=100)
# cyc = Evolution.Cycle([select_p, mut_p, eval_p, record_p])
