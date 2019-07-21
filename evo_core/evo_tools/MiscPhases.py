from evo_core.Evolution import EvoPhase


class SimpleInitPhase(EvoPhase):
    def __init__(self, gen_limit):
        self.gen_number = 0
        self.gen_limit = gen_limit

    def run(self, population):
        self.gen_number = 0

        return population

    def check_gen_limit(self):
        ret_val = False if self.gen_number < self.gen_limit else True
        self.gen_number += 1
        return ret_val

    def __repr__(self):
        return "SimpleInitPhase gen_limit=%d" % self.gen_limit


class MaintainBestsPhase(EvoPhase):
    def __init__(self, fitness_getter_function, best_ever_ind=None):
        self.fitness_getter_function = fitness_getter_function
        self.best_ind = None
        self.best_ever_ind = best_ever_ind

    def run(self, population):
        self.best_ind = (max([ind for ind in population], key=lambda x: self.fitness_getter_function(x)))

        self.best_ever_ind = \
            self.best_ever_ind.self_replicate() \
                if self.best_ever_ind is not None \
                   and self.fitness_getter_function(self.best_ever_ind) > self.fitness_getter_function(self.best_ind) \
                else self.best_ind.self_replicate()

        return population

    def __repr__(self):
        return "MaintainBestsPhase"


class MaintainRecordBestsPhase(EvoPhase):
    def __init__(self, fitness_getter_function, best_ever_ind=None, out_file_path=None, debug_output=False):
        self.gen_number = 0
        self.fitness_getter_function = fitness_getter_function
        self.best_ind = None
        self.best_ever_ind = best_ever_ind
        self.out_file_path = out_file_path
        if self.out_file_path is not None:
            out_file = open(out_file_path, 'w')
            out_file.close()
        self.debug_output = debug_output

    def restart(self, best_ever_ind=None, out_file_path=None, debug_output=False):
        self.gen_number = 0
        self.best_ever_ind = best_ever_ind
        if out_file_path != self.out_file_path:
            self.out_file_path = out_file_path
            if self.out_file_path is not None:
                out_file = open(out_file_path, 'w')
                out_file.close()
        self.debug_output = debug_output

    def run(self, population):
        if self.debug_output is True:
            print('\nGeneration ' + str(self.gen_number) + ':')
        self.best_ind = (max([ind for ind in population], key=lambda x: self.fitness_getter_function(x)))

        self.best_ever_ind = \
            self.best_ever_ind.self_replicate() \
                if self.best_ever_ind is not None \
                   and self.fitness_getter_function(self.best_ever_ind) > self.fitness_getter_function(self.best_ind) \
                else self.best_ind.self_replicate()

        if self.out_file_path is not None:
            with open(self.out_file_path, 'a') as f:
                f.write('\nGeneration ' + str(self.gen_number) + '\n')
                f.write('Best ind: ' + self.best_ind.compact_str_representation() + '\n')
                f.write('Fitness: ' + str(self.fitness_getter_function(self.best_ind)) + '\n')

        self.gen_number += 1

        return population

    def __repr__(self):
        return "MaintainBestsPhase"


