from abc import ABCMeta
import copy as cp
import evo_core.Population_Containers


class GPIndividual(evo_core.Population_Containers.Individual, metaclass=ABCMeta):
    funcs_array = []

    def __init__(self, genome):
        self.genome = cp.deepcopy(genome)

    def develop(self):
        return cp.deepcopy(self.genome)

    def self_replicate(self):
        # There may be a need to manipulate code somewhere else to ensure development.
        return cp.deepcopy(self)

    @classmethod
    def add_function_node(cls, func):
        cls.funcs_array.append(func)

    @classmethod
    def add_function_nodes(cls, funcs):
        for func in funcs:
            cls.add_function_node(func)

    pass

