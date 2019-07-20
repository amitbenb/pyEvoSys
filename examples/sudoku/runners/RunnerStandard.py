import time as t

import numpy as np

import evo_core.Evolution as Evolution
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.EvoParams as EPs
import examples.sudoku.runners.RunParams as RPs

if __name__ == "__main__":

    for i in range(RPs.number_of_simulations):
        init_p = MiscPhases.SimpleInitPhase(EPs.num_of_generations)

        out_file_path = RPs.out_path + 'out' + str(i).zfill(3) + '.txt'
        record_p = MiscPhases.MaintainRecordBestsPhase(EPs.get_fitness, out_file_path=out_file_path,
                                                       debug_output=BoardGen.DEBUG_OUTPUT)

        # cyc = Evolution.Cycle(
        #     [EPs.elite_e_p, EPs.select_p, EPs.mut_p, EPs.elite_m_p, EPs.eval_p, record_p, save_solutions_p])
        # cyc = Evolution.Cycle([EPs.elite_e_p, EPs.select_p, EPs.mut_p, EPs.gxo_p, EPs.elite_m_p, EPs.eval_p, record_p,
        #                        save_solutions_p])
        cyc = Evolution.Cycle(
            [EPs.select_p, EPs.mut_p, EPs.gmut_p, EPs.eval_p, record_p, EPs.save_solutions_p, EPs.distorter_p])
        # cyc = Evolution.Cycle(
        #     [EPs.elite_e_p, EPs.null_select_p, EPs.mut_p, EPs.eval_p, EPs.gxo_p, EPs.elite_m_p, EPs.eval_p, record_p,
        #      save_solutions_p])
        ebody = Evolution.EpochBasicBody(cyc, init_p.check_gen_limit)
        init_cyc = Evolution.Cycle([EPs.init_p, EPs.eval_p, record_p, EPs.save_solutions_p])
        epo = Evolution.Epoch(ebody, init_cycle=init_cyc)
        evo = Evolution.Evolution(epo)

        if i == 0:
            with open(RPs.experiment_big_fit_out_file_name, 'w') as fit_f:
                fit_f.write("Sim#, Best_fitness\n")

        _t1 = t.time()
        evo.run(EPs.pop)
        _t2 = t.time()

        print("Runtime: " + str(_t2 - _t1))

        with open(RPs.experiment_big_fit_out_file_name, 'a') as fit_f:
            fit_f.write(str(i).zfill(3) + ', ' + str(record_p.best_ever_ind.get_fitness()) + '\n')

        with open(RPs.solution_file_name + str(i).zfill(3) + '.txt', 'w') as sol_f:
            sol_f.write('Number of solutions = ' + str(len(EPs.save_solutions_p.solutions)) + '\n\n')
            for sol in EPs.save_solutions_p.solutions:
                sol_f.write(str(sol) + '\n\n')
    pass
