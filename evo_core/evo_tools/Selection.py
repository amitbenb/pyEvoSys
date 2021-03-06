import math
import random as rn

from evo_core.Evolution import EvoPhase
from evo_core import Population_Containers


class SimpleNullSelectionPhase(EvoPhase):
    def __init__(self, target_length=None):
        # super(TournamentSelectionPhase, self).__init__()
        self.target_length = target_length

    def run(self, population):
        population: Population_Containers.SimplePopulation
        # pop = [i.self_replicate() for i in population]
        new_pop = []
        if self.target_length is None:
            self.target_length = len(population)

        while len(new_pop) < self.target_length:
            new_pop += [i for i in population]
            # new_pop += cp.deepcopy(self.select_best(rn.sample(pop, self.tour_size)))
        new_pop = rn.sample(new_pop, self.target_length)

        return population.update_pop([i.self_replicate() for i in new_pop])

    def __str__(self):
        return "SimpleNullSelectionPhase target_length=%d" % self.target_length


class SimpleExtractElitePhase(EvoPhase):
    def __init__(self, fitness_getter_function, elite_size=5, use_ratio=False, clone_max=None):
        """

        :param fitness_getter_function:
        :param elite_size:  Size of Elite (or ratio. see below).
        :param use_ratio:   (Flag) Is ratio used instead of size (0.01 of population rather than 2 individuals).
        :param clone_max:   (Not implemented) Number of clones of single individual allowed in elite.
        """
        self.fitness_getter_function = fitness_getter_function
        self.elite_ratio = self.elite_size = elite_size
        self.use_ratio = use_ratio
        self.clone_max = clone_max
        pass

    def run(self, population):
        population:Population_Containers.SimplePopulationWithElite
        # print(len(population))
        if self.use_ratio:
            elite_size = self.elite_ratio * len(population)
        else:
            elite_size = self.elite_size
        elite_size = min(self.elite_size, len(population))
        pop = sorted(population, key=lambda x: self.fitness_getter_function(x), reverse=True)

        population.elite = pop[:elite_size]
        population.update_pop(pop[elite_size:])

        # print(len(population), len(population.elite))

        return population

    def __repr__(self):
        if self.elite_ratio is True:
            return "SimpleExtractElitePhase elite_ratio=%.3f clone_max=%s" % (self.elite_ratio, self.clone_max)
        else:
            return "SimpleExtractElitePhase elite_size=%d clone_max=%s" % (self.elite_size, self.clone_max)


class SimpleMergeElitePhase(EvoPhase):
    def __init__(self):
        pass

    def run(self, population):
        population: Population_Containers.SimplePopulationWithElite

        # print(len(population), len(population.elite), len(population.get_everyone()))
        # print(population.get_everyone() == population.pop)
        population.update_pop(population.get_everyone())

        return population

    def __repr__(self):
        return "SimpleMergeElitePhase"


class TournamentSelectionPhase(EvoPhase):
    def __init__(self, fitness_getter_function, tour_size=2, tour_winners=1, target_length=None):
        # super(TournamentSelectionPhase, self).__init__()
        self.fitness_getter_function = fitness_getter_function
        self.tour_size = tour_size
        self.tour_winners = tour_winners
        self.target_length = target_length

    def run(self, population):
        population: Population_Containers.SimplePopulation
        pop = population.get_everyone()
        # pop = [i.self_replicate() for i in population]
        new_pop = []
        if self.target_length is None:
            self.target_length = len(population)

        while len(new_pop) < self.target_length:
            new_pop += [i.self_replicate() for i in self.select_best(rn.sample(pop, self.tour_size))]
            # new_pop += cp.deepcopy(self.select_best(rn.sample(pop, self.tour_size)))
        new_pop = new_pop[:self.target_length]

        return population.update_pop([i.self_replicate() for i in new_pop])
        # return population.update_pop(cp.deepcopy(new_pop))

    def select_best(self, tournament):
        # z = sorted(tournament, key=lambda x: self.fitness_getter_func(x), reverse=True)
        # print([i.genome for i in z])
        # print([self.fitness_getter_func(i) for i in z])
        # print(self.fitness_getter_function(
        #     sorted(tournament, key=lambda x: self.fitness_getter_function(x), reverse=True)[:self.tour_winners][-1]))
        # print(self.fitness_getter_function(
        #     sorted(tournament, key=lambda x: self.fitness_getter_function(x), reverse=True)[0]),
        #       self.fitness_getter_function(
        #           sorted(tournament, key=lambda x: self.fitness_getter_function(x), reverse=True)[0]))
        return sorted(tournament, key=lambda x: self.fitness_getter_function(x), reverse=True)[:self.tour_winners]

    def __repr__(self):
        return "TournamentSelectionPhase tour_size=%d winners=%d target_length=%s" % (
            self.tour_size, self.tour_winners, self.target_length)


class BinnedTournamentSelectionPhase(TournamentSelectionPhase):
    def __init__(self, fitness_getter_function, tour_size=2, tour_winners=1, binning_func=None):
        super().__init__(fitness_getter_function, tour_size, tour_winners)
        # self.fitness_getter_function = fitness_getter_function
        # self.tour_size = tour_size
        # self.tour_winners = tour_winners
        # self.target_length = target_length
        self.binning_func = binning_func if binning_func is not None else (lambda x: [list(x)])

        pass

    def run(self, population):
        population: Population_Containers.SimplePopulation
        pop = population.get_everyone()
        # pop = [i.self_replicate() for i in population]
        new_pop = []
        self.target_length = len(population)
        binned_pop = self.binning_func(pop)
        binned_pop = [i for i in binned_pop if len(i) > 0]

        print(len(binned_pop), [len(i) for i in binned_pop])

        for bin0 in binned_pop:
            selected_inds = []
            bin_length_after_selection = int(math.ceil(self.target_length / len(binned_pop)))
            while len(selected_inds) < bin_length_after_selection:
                selected_inds += [i.self_replicate() for i in
                                  self.select_best(rn.sample(bin0, min(self.tour_size, len(bin0))))]
            new_pop += selected_inds[:bin_length_after_selection]

        # print(len(new_pop), self.target_length)
        new_pop = rn.sample(new_pop, self.target_length)

        return population.update_pop([i.self_replicate() for i in new_pop])

    def __repr__(self):
        return "BinnedTournamentSelectionPhase tour_size=%d winners=%d target_length=%s" % (
            self.tour_size, self.tour_winners, self.target_length)


class SimpleCloneLimitingPhase(EvoPhase):
    def __init__(self, clone_max=5):
        self.clone_max = clone_max

    def run(self, population):
        population: Population_Containers.SimplePopulation

        new_pop = []

        # while len(new_pop) < len(population):  # This is correct but brings the infinite loop
        for _ in range(3):
            for idx, itm in enumerate(population):
                if len(new_pop) < len(population) and len([x for x in new_pop if x == itm]) < self.clone_max:
                    new_pop.append(itm)
            if len(new_pop) >= len(population):
                break

        # Loop of last resort to fill in population.
        while len(new_pop) < len(population):
            new_pop.append(rn.choice(new_pop))

        return population.update_pop(new_pop)

    def __repr__(self):
        return "SimpleCloneLimitingPhase clone_max=%d" % self.clone_max


