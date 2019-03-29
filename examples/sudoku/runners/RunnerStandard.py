import numpy as np

import evo_core.Population_Containers as PopContainers
import evo_core.Evolution as Evolution

from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen

if __name__ == "__main__":
    num_of_generations = 10
    pop_size = 100
    size = BoardGen.BOARD_SIZE
    # print(np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size))))
    # input()
    inds = [BoardGen.BoardGenIndividual(
        genome=np.concatenate(tuple(np.random.permutation(range(1, size + 1)) for _ in range(size))),
        size=size)
        for _ in range(pop_size)]

    # pop = PopContainers.SimplePopulation()
    pop = PopContainers.SimplePopulationWithElite()
    pop.update_pop(inds)

    get_fitness = BoardGen.BoardGenIndividual.get_fitness
    calculate_fitness = BoardGen.BoardGenIndividual.calculate_fitness
    init_p = MiscPhases.SimpleInitPhase(num_of_generations)
    select_p = Selection.TournamentSelectionPhase(get_fitness, tour_size=4)
    mut_p = BoardGen.SwapMutationPhase(probability=0.8)
    eval_p = BoardGen.FitnessEvaluationPhase()
    record_p = MiscPhases.MaintainRecordBestsPhase(get_fitness, out_file_path='output/out.txt')
    elite_e_p = Selection.SimpleExtractElitePhase(get_fitness, elite_size=4)
    elite_m_p = Selection.SimpleMergeElitePhase()
    # cyc = Evolution.Cycle([select_p, mut_p, eval_p, record_p])
    cyc = Evolution.Cycle([elite_e_p, select_p, mut_p,  elite_m_p, eval_p, record_p])
    ebody = Evolution.EpochBasicBody(cyc, init_p.check_gen_limit)
    epo = Evolution.Epoch(ebody, init_cycle=Evolution.Cycle([init_p, eval_p, record_p]))
    evo = Evolution.Evolution(epo)

    evo.run(pop)

    pass
