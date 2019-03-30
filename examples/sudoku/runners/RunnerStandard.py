import time as t

import numpy as np

import evo_core.Evolution as Evolution
from evo_core.evo_tools import MiscPhases

import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.EvoParams as EPs
import examples.sudoku.runners.RunParams as RPs

if __name__ == "__main__":
    record_p = MiscPhases.MaintainRecordBestsPhase(EPs.get_fitness, out_file_path= RPs.out_path + 'out.txt',
                                                   debug_output=BoardGen.DEBUG_OUTPUT)

    cyc = Evolution.Cycle([EPs.elite_e_p, EPs.select_p, EPs.mut_p, EPs.elite_m_p, EPs.eval_p, record_p])
    ebody = Evolution.EpochBasicBody(cyc, EPs.init_p.check_gen_limit)
    epo = Evolution.Epoch(ebody, init_cycle=Evolution.Cycle([EPs.init_p, EPs.eval_p, record_p]))
    evo = Evolution.Evolution(epo)

    _t1 = t.time()
    evo.run(EPs.pop)
    _t2 = t.time()

    print("Runtime: " + str(_t2 - _t1))

    pass
