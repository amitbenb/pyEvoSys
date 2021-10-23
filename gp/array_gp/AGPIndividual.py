from abc import ABCMeta
import random as rand
import copy as cp
from evo_core.evo_tools import Individuals as inds
from gp.GPIndividual import GPIndividual


class AGPIndividual(inds.VectorIndividual, GPIndividual):
    minimum_float, maximum_float = 0.0, 1.0

    def __init__(self, genome=None):
        super(AGPIndividual,self).__init__(genome)
        self.phenome = self.genome

    # def set_tree(self, node):
    #     self.root = node

    def __str__(self):
        return self.str_rec(self.get_root())

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

        if 'random_node_func' not in grow_params:
            grow_params['random_node_func'] = self.__class__.return_random_node

        if 'random_terminal_func' not in grow_params:
            grow_params['random_terminal_func'] = self.__class__.return_random_terminal

        if 'random_func_func' not in grow_params:
            grow_params['random_func_func'] = self.__class__.return_random_function

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
        return 0.0

    def generate_new_gene_sequence(self, length):
        ret_val = []
        for i in range(length):
            ret_val.append(self.__class__.return_random_node())
        # print(self.max_int, 'X', ret_val)
        return ret_val

    @classmethod
    def get_func(cls, node_code):
        # TODO: TODO or to overload.
        funcs_array = cls.funcs_array
        index = int(len(funcs_array) * (node_code - cls.minimum_float) / cls.get_float_range_size())
        # print(node_code, len(funcs_array), index)
        # input()
        return funcs_array[index]

    @classmethod
    def get_float_range_size(cls):
        return cls.maximum_float - cls.minimum_float

    @classmethod
    def return_random_node(cls):
        return {'value': cls.random_float_content(),
                'Terminal': rand.choice([False for _ in range(4)] + [True])}

    @classmethod
    def return_random_terminal(cls):
        return {'value': cls.random_float_content(), 'Terminal': True}

    @classmethod
    def return_random_function(cls):
        return {'value': cls.random_float_content(), 'Terminal': False}

    @classmethod
    def random_float_content(cls, min_f=None, max_f=None):
        # print(max_f, cls.maximum_float)
        # print((max_f - min_f) + min_f)
        if min_f is None:
            min_f = cls.get_minimum_float()
        if max_f is None:
            max_f = cls.get_maximum_float()

        return rand.random() * (max_f - min_f) + min_f

    @classmethod
    def get_minimum_float(cls):
        return cls.minimum_float

    @classmethod
    def get_maximum_float(cls):
        return cls.maximum_float

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

    def str_rec(self, index):
        node: dict = self.phenome[index] if index < len(self) else {}

        if node == {}:
            return str(self.get_default_value())
        elif self.is_terminal(node):
            return str(self.get_node_value(node))
        else:
            func = self.get_func(self.get_node_value(node))
            args_nodes = self.get_node_children(node)  # Nodes for arguments of function
            args_names = tuple([self.str_rec(self.get_index(index, arg)) for arg in args_nodes])  # Arguments of function
            return '(' + func.__name__ + ', ' + ', '.join(args_names) +')'

    def get_node_value(self, node):
        """
        :param node: Assumed to be a dictionary with 'value' field (probably containing a float)
        :return: value returned by node

        """
        return node['value']

    def is_terminal(self, node):
        """
        :param node: Assumed to be a dictionary with boolean 'Terminal' field
        :return: if node is marked as terminal
        """

        return node["Terminal"]

    def get_node_children(self, node, default=('l', 'r')):
        return sorted(node.get('children', ('l', 'r')))

# class GPNode(metaclass=ABCMeta):
#     # def __init__(self):
#     #     raise NotImplementedError()
#
#     def grow(self, parent=None):
#         raise NotImplementedError()
