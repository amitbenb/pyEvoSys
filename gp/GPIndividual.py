from abc import ABCMeta
import copy as cp
import evo_core.Population_Containers


class GPIndividual(evo_core.Population_Containers.Individual, metaclass=ABCMeta):
    typed_flag = False
    types_array = [float]
    funcs_arrays = [] if typed_flag is False else {t: [] for t in types_array}
    terminals_arrays = [] if typed_flag is False else {t: [] for t in types_array}

    def __init__(self, genome):
        self.genome = cp.deepcopy(genome)

    def develop(self):
        return cp.deepcopy(self.genome)

    def self_replicate(self):
        # There may be a need to manipulate code somewhere else to ensure development.
        return cp.deepcopy(self)

    @classmethod
    def add_function_node(cls, func, f_type=type(None)):
        cls.funcs_arrays.append(func)

    @classmethod
    def add_function_nodes(cls, funcs, f_type=type(None)):
        for func in funcs:
            cls.add_function_node(func)

    @classmethod
    def add_terminal_node(cls, term, f_type=type(None)):
        cls.terminals_arrays.append(term)

    @classmethod
    def add_terminal_nodes(cls, terms, f_type=type(None)):
        for term in terms:
            cls.add_terminal_node(term)

    pass

