import time as t

import numpy as np

import evo_core.Evolution as Evolution
from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.runners.RunnerCore as RC
import examples.sudoku.EvoParams as EPs
import examples.sudoku.runners.RunParams as RPs

import examples.sudoku.SudokuBinning as Binning

if __name__ == "__main__":

    binning_function = lambda x: Binning.hash_based_binning(x, EPs.size, number_of_bins)
    select_p = Selection.BinnedTournamentSelectionPhase(EPs.get_fitness, tour_size=EPs.tour_size,
                                                        tour_winners=EPs.tour_winners, binning_func=binning_function)
    _t1 = t.time()

    for i in range(RPs.number_of_simulations):
        init_p = MiscPhases.SimpleInitPhase(EPs.num_of_generations)
        number_of_bins = int(np.sqrt(EPs.pop_size))

        out_file_path = RPs.out_path + 'out' + str(number_of_bins) + 'bins' + str(i).zfill(3) + '.txt'
        record_p = MiscPhases.MaintainRecordBestsPhase(EPs.get_fitness, out_file_path=out_file_path,
                                                       debug_output=BoardGen.DEBUG_OUTPUT)

        EPs.save_solutions_p.restart()

        # cyc = Evolution.Cycle(
        #     [EPs.elite_e_p, select_p, EPs.mut_p, EPs.elite_m_p, EPs.eval_p, record_p, save_solutions_p])
        cyc = Evolution.Cycle(
            [select_p, EPs.mut_p, EPs.gmut_p, EPs.eval_p, record_p, EPs.save_solutions_p, EPs.distorter_p])
        # print([i for i in cyc])
        ebody = Evolution.EpochBasicBody(cyc, EPs.init_p.check_gen_limit)
        init_cyc = Evolution.Cycle([EPs.pop_init_p, EPs.init_p, EPs.eval_p, record_p, EPs.save_solutions_p])
        epo = Evolution.Epoch(ebody, init_cycle=init_cyc)
        evo = Evolution.Evolution(epo)

        if i == 0:
            # with open(RPs.experiment_big_fit_out_file_name, 'w') as fit_f:
            #     fit_f.write("Sim#, Best_fitness\n")
            RC.write_experiment_preamble(init_cyc, cyc, None)

        _t2 = t.time()
        evo.run(EPs.pop)
        _t3 = t.time()

        print("Runtime: " + str(_t3 - _t2))

        with open(RPs.experiment_big_fit_out_file_name, 'a') as fit_f:
            # Writing line in fitness file
            fit_f.write(str(i).zfill(3) + ', ')
            fit_f.write(str(record_p.best_ever_ind.get_fitness()) + ', ')
            fit_f.write(str(len(EPs.save_solutions_p.solutions)) + '\n')

        with open(RPs.solution_file_name + str(i).zfill(3) + '.txt', 'w') as sol_f:
            sol_f.write("Runtime: " + str(_t3 - _t2) + "\n")
            sol_f.write('Number of solutions = ' + str(len(EPs.save_solutions_p.solutions)) + '\n\n')
            for sol in EPs.save_solutions_p.solutions:
                sol_f.write(str(sol) + '\n\n')

    _t4 = t.time()
    print("Total runtime: " + str(_t4 - _t1))
    pass
