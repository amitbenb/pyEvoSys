from abc import ABCMeta
import copy as cp


class Population(metaclass=ABCMeta):
    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __getitem__(self, item):
        raise NotImplementedError()
    
    def update_pop(self, new_pop):
        raise NotImplementedError()


class SimplePopulation(Population):
    pop: list

    def __init__(self, pop=[]):
        super(SimplePopulation, self).__init__()
        self.pop = pop

    def get_everyone(self):
        return list(self.pop)

    def __iter__(self):
        return iter(self.pop)

    def __len__(self):
        return len(self.pop)

    def __getitem__(self, item):
        return list(self.pop).__getitem__(item)

    def update_pop(self, new_pop):
        self.pop = [i.self_replicate() for i in new_pop]
        # self.pop = []
        # for idx, itm in enumerate(new_pop):
        #     self.pop.append(cp.deepcopy(itm))
        return self


class SimplePopulationWithElite(SimplePopulation):
    def __init__(self, pop=[], elite=[]):
        super(SimplePopulationWithElite, self).__init__(pop)
        self.elite = elite
        # self.elite = [i.self_replicate() for i in elite]

    # def __iter__(self):
    #     return iter(list(self.elite) + list(self.pop))

    def get_everyone(self):
        return list(self.elite) + list(self.pop)

    def elite_len(self):
        return len(self.elite)

    def total_len(self):
        return self.elite_len() + self.__len__()

    def __getitem__(self, item):
        return list(self.pop).__getitem__(item)

    # def update_pop(self, new_pop):
    #     self.pop = [i.self_replicate() for i in new_pop]
    #     return self


class Individual(metaclass=ABCMeta):
    def self_replicate(self):
        raise NotImplementedError()

    def compact_str_representation(self):
        return str(self)

