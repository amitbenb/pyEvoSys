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

from gp.array_gp.AGPIndividual import AGPIndividual
from gp.GPIndividual import GPIndividual
import random as rand

AGPIndividual.minimum_float = 0.0
AGPIndividual.maximum_float = 2.0


class NumericalTargetIndividual(AGPIndividual):
    def __init__(self, genome=None, target=0.0):
        super(NumericalTargetIndividual, self).__init__(genome)
        self.fitness = float('-inf')
        self.target = target

    def calculate_fitness(self):
        self.develop()
        self.fitness = float(10 - abs(self.run() - self.target))
        return self.fitness

    def get_fitness(self):
        return self.fitness

    # @classmethod
    # def get_func(cls, node_code):
    #     def add(a, b): return a + b
    #     def sub(a, b): return a - b
    #     def plus01(a, b): return a + 0.1 * b
    #     def minus01(a, b): return a - 0.1 * b
    #
    #     func_array = [add, sub, plus01, minus01]
    #     index = int(len(func_array) * (node_code - cls.minimum_float) / cls.get_float_range_size())
    #     return func_array[index]


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
    def plus01(a, b): return a + 0.1 * b
    def minus01(a, b): return a - 0.1 * b

    import gp.GP_Basic_Functions as fs
    GPIndividual.add_function_nodes([plus01, minus01, fs.sub, fs.add])
    # GPIndividual.add_function_node(plus01)
    # GPIndividual.add_function_node(minus01)

    numerical_target = 14.3
    num_of_generations = 100
    pop_size = 100
    genome_len = 63
    inds = [NumericalTargetIndividual(target=numerical_target) for _ in range(pop_size)]
    grow_params = {
        'grow_type': 'Random',
        'size': genome_len
        # 'random_node_func': return_random_node,
        # 'random_func_func': return_random_terminal,
        # 'random_terminal_func': return_random_function
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

