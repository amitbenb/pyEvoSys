from abc import ABCMeta
import random as rand
from evo_core.evo_tools import Individuals as inds


class GPArray(inds.VectorIndividual):
    def __init__(self, genome=None):
        super.__init__(genome)
        # self.root = node

    # def set_tree(self, node):
    #     self.root = node

    def grow(self, grow_params={}):
        """
        :param grow_params: dictionary of parameters for tree grow function.
        :return: In inherited classes type of node that tree builds is known
        """

        match grow_params.get('grow_type', 0):
            case 'Random':
                self.grow_random(grow_params)
                pass
            case 'Full':
                self.grow_full(grow_params)
                pass
            case 'Height limited':
                self.grow_height(grow_params)
                pass
            # case 'Ramped Half':
            #     raise NotImplementedError()
            #     pass
            case _:
                self.grow_random(grow_params)
                pass

    def grow_random(self, grow_params):
        size = grow_params['size']
        inner_size = (size + 1) // 2
        self.genome = [grow_params['random_node_func']() for i in range(inner_size)] + [
            grow_params['random_terminal_func']() for i in range(inner_size, size)]

    def grow_full(self, grow_params):
        size = grow_params['size']
        inner_size = (size + 1) // 2
        size = grow_params['size']
        self.genome = [grow_params['random_func_func']() for i in range(inner_size)] + [
            grow_params['random_terminal_func']() for i in range(inner_size, size)]

    def grow_height(self, grow_params):
        size = grow_params['size']
        height = grow_params['Height limit']
        inner_size = min((size + 1) // 2, (2 ** height) - 1)
        self.genome = [grow_params['random_node_func']() for i in range(inner_size)] + [
            grow_params['random_terminal_func']() for i in range(inner_size, size)]


# class GPNode(metaclass=ABCMeta):
#     # def __init__(self):
#     #     raise NotImplementedError()
#
#     def grow(self, parent=None):
#         raise NotImplementedError()
