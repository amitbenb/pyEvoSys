from abc import ABCMeta
import random as rand
import copy as cp
from evo_core.evo_tools import Individuals as inds


class AGPIndividual(inds.VectorIndividual):
    def __init__(self, genome=None):
        super(AGPIndividual,self).__init__(genome)
        self.phenome = self.genome

    # def set_tree(self, node):
    #     self.root = node

    def get_root(self):
        return 0  # default index of root

    def develop(self):
        self.phenome = cp.deepcopy(self.genome)
        return cp.deepcopy(self.genome)

    def run(self):
        return self.run_rec(self.get_root())

    def run_rec(self, index):
        # print(index)

        node: dict = self.phenome[index] if index < len(self) else {}

        # print(index, node, node == {})
        if node == {}:
            return self.get_default_value()
        elif node['Terminal']:
            return node['value']
        else:
            func = self.get_func(node['value'])
            args_nodes = sorted(node.get('children', ('l', 'r')))  # Nodes for arguments of function
            args = tuple([self.run_rec(self.get_index(index, arg)) for arg in args_nodes])  # Arguments of function
            return func(*args)

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

    def get_default_value(self):
        return 0

    def get_func(self, node_code):
        # TODO: TODO or to overload.
        return lambda *args: None

    def get_index(self, starting_index, arg):
        index = starting_index
        for ch in arg:
            if ch == 'l':
                index = index * 2 + 1
            elif ch == 'r':
                index = index * 2 + 2
            else:
                raise RuntimeError('child is not denoted as left (l) or right (r). Rather: ' + ch)

        return index

# class GPNode(metaclass=ABCMeta):
#     # def __init__(self):
#     #     raise NotImplementedError()
#
#     def grow(self, parent=None):
#         raise NotImplementedError()
