import time as t

import numpy as np

# import examples.sudoku.BoardGen as BoardGen
import examples.sudoku.EvoParams as EPs
import examples.sudoku.runners.RunParams as RPs


def write_experiment_preamble(init_cycle, cycle, end_cycle):
    with open(RPs.experiment_big_fit_out_file_name, 'w') as fit_f:
        fit_f.write("Number of simulations: " + str(RPs.number_of_simulations) + "\n")
        fit_f.write("Size of board: " + str(EPs.size) + "\n")

        if init_cycle is not None:
            fit_f.write("Initialization cycle: " + "\n")
            write_cycle(fit_f, init_cycle)
            # for i in init_cycle:
            #     fit_f.write('\t' + str(i) + '\n')
            # fit_f.write('\n')

        if cycle is not None:
            fit_f.write("Main cycle: " + "\n")
            write_cycle(fit_f, cycle)

        if end_cycle is not None:
            fit_f.write("End cycle: " + "\n")
            write_cycle(fit_f, end_cycle)

        fit_f.write("Population size: " + str(EPs.pop_size) + "\n")
        fit_f.write("Number of generations: " + str(EPs.num_of_generations) + "\n")
        fit_f.write("\nSim#, Best_fitness, #_of_Solutions\n")


def write_cycle(out_file, cycle):
    for i in cycle:
        out_file.write('\t' + repr(i) + '\n')
    out_file.write('\n')
