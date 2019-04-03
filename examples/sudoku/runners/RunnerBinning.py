import time as t

import numpy as np

import evo_core.Evolution as Evolution
from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.EvoParams as EPs
import examples.sudoku.SudokuBinning as Binning
import examples.sudoku.runners.RunParams as RPs

if __name__ == "__main__":

    with open(RPs.experiment_big_fit_out_file_name, 'w') as fit_f:
        fit_f.write("Sim#, Best_fitness\n")

    binning_function = lambda x: Binning.hash_based_binning(x, EPs.size, number_of_bins)
    select_p = Selection.BinnedTournamentSelectionPhase(EPs.get_fitness, tour_size=EPs.tour_size,
                                                        binning_func=binning_function)
    for i in range(RPs.number_of_simulations):
        init_p = MiscPhases.SimpleInitPhase(EPs.num_of_generations)
        number_of_bins = int(np.sqrt(EPs.pop_size))

        out_file_path = RPs.out_path + 'out' + str(number_of_bins) + 'bins' + str(i).zfill(3) + '.txt'
        record_p = MiscPhases.MaintainRecordBestsPhase(EPs.get_fitness, out_file_path=out_file_path,
                                                       debug_output=BoardGen.DEBUG_OUTPUT)
        save_solutions_p = BoardGen.SaveSolutionsPhase()

        cyc = Evolution.Cycle(
            [EPs.elite_e_p, select_p, EPs.mut_p, EPs.elite_m_p, EPs.eval_p, record_p, save_solutions_p])
        ebody = Evolution.EpochBasicBody(cyc, EPs.init_p.check_gen_limit)
        epo = Evolution.Epoch(ebody, init_cycle=Evolution.Cycle([EPs.init_p, EPs.eval_p, record_p, save_solutions_p]))
        evo = Evolution.Evolution(epo)

        _t1 = t.time()
        evo.run(EPs.pop)
        _t2 = t.time()

        print("Runtime: " + str(_t2 - _t1))

        with open(RPs.experiment_big_fit_out_file_name, 'a') as fit_f:
            fit_f.write(str(i).zfill(3) + ', ' + str(record_p.best_ever_ind.get_fitness()) + '\n')

        with open(RPs.solution_file_name + str(i).zfill(3) + '.txt', 'w') as sol_f:
            sol_f.write('Number of solutions = ' + str(len(save_solutions_p.solutions)) + '\n\n')
            for sol in save_solutions_p.solutions:
                sol_f.write(str(sol) + '\n\n')
    pass
