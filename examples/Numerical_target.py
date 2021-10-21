"""
Domain for (Array) GP
Terminals are numbers
Functions are arithmetic operators.
fitness #1 distance from target.
"""

import evo_core.Evolution as Evolution
import evo_core.Population_Containers as PopContainers
from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases
from evo_core.evo_tools.MiscPhases import SimpleInitPhase

from gp.array_gp import AGPIndividual
import random as rand


minimum_float, maximum_float = 0.0, 2.0
float_range_size = maximum_float - minimum_float


class NumericalTargetIndividual(AGPIndividual.AGPIndividual):
    def __init__(self, genome=None, target=0.0):
        super(NumericalTargetIndividual, self).__init__(genome)
        self.fitness = float('-inf')
        self.target = target

    def generate_new_gene_sequence(self, length):
        ret_val = []
        for i in range(length):
            ret_val.append(return_random_node())
        # print(self.max_int, 'X', ret_val)
        return ret_val

    def calculate_fitness(self):
        self.develop()
        self.fitness = float(10 - abs(self.run() - self.target))
        return self.fitness

    def get_fitness(self):
        return self.fitness

    def get_func(self, node_code):
        # TODO: TODO or to overload.
        def plus(a, b): return a + b
        def minus(a, b): return a - b
        def plus01(a, b): return a + 0.1 * b
        def minus01(a, b): return a - 0.1 * b

        func_array = [
            plus, minus, plus01, minus01
            # lambda a, b: a + b,
            # lambda a, b: a - b,
            # lambda a, b: a + b * 0.1,
            # lambda a, b: a - b * 0.1
        ]
        index = int(len(func_array) * (node_code - minimum_float) / float_range_size)
        return func_array[index]


def random_float_content(min_f=minimum_float, max_f=maximum_float):
    return rand.random() * (max_f - min_f) + min_f


def return_random_node():
    return {'value': random_float_content(), 'Terminal': rand.choice([False for _ in range(4)] + [True])}


def return_random_terminal():
    return {'value': random_float_content(), 'Terminal': True}


def return_random_function():
    return {'value': random_float_content(), 'Terminal': False}


class UMutationPhase(Evolution.EvoPhase):

    def run(self, population):
        for ind in population:
            ind.perform_uniform_plus_mutation()

        return population


class FitnessEvaluationPhase(Evolution.EvoPhase):

    def run(self, population):
        for ind in population:

            ind.calculate_fitness()
            # if rn.random() < 1:
            #     print("%s %.0f" % (str(ind.genome), ind.get_fitness()))

        return population


if __name__ == "__main__":
    numerical_target = 14.3
    num_of_generations = 100
    pop_size = 100
    genome_len = 30
    inds = [NumericalTargetIndividual(target=numerical_target) for _ in range(pop_size)]
    grow_params = {
        'grow_type': 'Random',
        'size': 15,
        'random_node_func': return_random_node,
        'random_func_func': return_random_terminal,
        'random_terminal_func': return_random_function
    }
    for ind in inds:
        ind.grow(grow_params)
    # pop = PopContainers.SimplePopulation()
    pop = PopContainers.SimplePopulationWithElite()
    pop.update_pop(inds)

    get_fitness = NumericalTargetIndividual.get_fitness
    init_p = SimpleInitPhase(num_of_generations)
    select_p = Selection.TournamentSelectionPhase(get_fitness, tour_size=2)
    mut_p = UMutationPhase()
    eval_p = FitnessEvaluationPhase()
    record_p = MiscPhases.MaintainRecordBestsPhase(get_fitness, out_file_path='output/out.txt')
    elite_e_p = Selection.SimpleExtractElitePhase(get_fitness, elite_size=2)
    elite_m_p = Selection.SimpleMergeElitePhase()
    # cyc = Evolution.Cycle([select_p, mut_p, eval_p, record_p])
    cyc = Evolution.Cycle([elite_e_p, select_p, mut_p,  elite_m_p, eval_p, record_p])
    ebody = Evolution.EpochBasicBody(cyc, init_p.check_gen_limit)
    epo = Evolution.Epoch(ebody, init_cycle=Evolution.Cycle([init_p, eval_p, record_p]))
    evo = Evolution.Evolution(epo)

    evo.run(pop)

    pass

