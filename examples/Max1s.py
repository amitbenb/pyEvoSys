import random as rn
import copy as cp

import evo_core.Evolution as Evolution
import evo_core.Population_Containers as PopContainers
from evo_core.evo_tools import Individuals
from evo_core.evo_tools import Selection
from evo_core.evo_tools import MiscPhases
from evo_core.evo_tools.MiscPhases import SimpleInitPhase


class Max1individual(Individuals.IntVectorIndividual):
    def __init__(self, genome):
        super(Max1individual, self).__init__(genome, 2)
        self.fitness = self.genome.count(1)

    def self_replicate(self):
        return cp.deepcopy(self)

    def calculate_fitness(self):
        self.fitness = float(self.genome.count(1))
        return self.fitness

    def get_fitness(self):
        return self.fitness

    def __str__(self):
        return str(self.genome)


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
    num_of_generations = 100
    pop_size = 25
    genome_len = 50
    inds = [Max1individual([rn.randint(0, 1) for _ in range(genome_len)]) for _ in range(pop_size)]
    # pop = PopContainers.SimplePopulation()
    pop = PopContainers.SimplePopulationWithElite()
    pop.update_pop(inds)

    get_fitness = Max1individual.get_fitness
    init_p = SimpleInitPhase(num_of_generations)
    select_p = Selection.TournamentSelectionPhase(get_fitness, tour_size=4)
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
