from abc import ABCMeta
from collections.abc import Iterable
import time as t

_debug_output_flag = False


class Evolution:
    def __init__(self, epochs):
        self.epochs = epochs if isinstance(epochs, Iterable) == list else [epochs]

    def run(self, population):
        epochs = self.epochs
        p = population

        for e in epochs:
            p = e.run(p)

        return p

    def documentation_list(self):
        return [self.__class__.__name__] + [ep.documentation_list() for ep in self.epochs]


class Epoch:
    def __init__(self, epoch_body, init_cycle=[], end_cycle=[]):
        self.epoch_body = epoch_body
        self.init_cycle = init_cycle
        self.end_cycle = end_cycle

    def run(self, population):
        p = population

        for ep in self.init_cycle:
            p = ep.run(p)

        p = self.epoch_body.run(p)

        for ep in self.end_cycle:
            p = ep.run(p)

        return p

    def documentation_list(self):
        return [self.__class__.__name__,
                Cycle(self.init_cycle).documentation_list(),
                self.epoch_body.documentation_list(),
                Cycle(self.end_cycle).documentation_list()]


class EpochBody(metaclass=ABCMeta):
    def run(self, population):
        raise NotImplementedError()

    def documentation_list(self):
        raise NotImplementedError()


class EpochBasicBody(EpochBody):
    def __init__(self, cycle, end_condition):
        self.cycle = cycle
        self.end_condition = end_condition
        self.cycle_counter = 0

    def run(self, population):
        p = population

        t1 = t.time()
        while not self.end_condition():
            if _debug_output_flag:
                t0 = t1
                t1 = t.time()
                print("\nProcessing Genenration #%d time %.3f\n" % (self.cycle_counter, t1-t0))
            p = self.cycle.run(p)
            # for ph in self.cycle:
            #     p = ph.run(p)
            self.cycle_counter += 1

        return p

    def documentation_list(self):
        return [self.__class__.__name__, [self.cycle.documentation_list()]]


class Cycle:
    def __init__(self, phases):
        self.phases = phases

    def __iter__(self):
        return iter(self.phases)

    def run(self, population):
        p = population
        for ph in self.phases:
            p = ph.run(p)

        return p

    def documentation_list(self):
        return [self.__class__.__name__ + str(len(self.phases))] \
               + [ph.documentation_list() for ph in self.phases]


class EvoPhase(metaclass=ABCMeta):
    def run(self, population):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__

    def documentation_list(self):
        rep = repr(self).split('\n')
        return rep
