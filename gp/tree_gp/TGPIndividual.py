from abc import ABCMeta
from gp import GPIndividual


class TGPIndividual(GPIndividual):
    def __init__(self, node=None):
        self.root = node

    def set_tree(self, node):
        self.root = node

    def grow(self, params):
        """
        :param params: parameters for tree grow function. use *params in call.
        :return: In inherited classes type of node that tree builds is known
        """
        raise NotImplementedError()


class GPNode(metaclass=ABCMeta):
    def __init__(self):
        raise NotImplementedError()

    def grow(self, parent=None):
        raise NotImplementedError()

