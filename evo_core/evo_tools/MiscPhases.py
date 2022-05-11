from evo_core.Evolution import EvoPhase
from evo_core.Evolution import Evolution


class SimpleInitPhase(EvoPhase):
    def __init__(self, gen_limit, pop_size='Undefined'):
        """
        This is a simple generic initialization phase for an evolutionary algorithm
        :param gen_limit: Number of generations defined for this initializtion.
        :param pop_size: Size of population defined for this initializtion.
                         Currently used only for output.
                         Default value for backwards compatibility
        """
        self.gen_number = 0
        self.gen_limit = gen_limit
        self.pop_size = pop_size if type(pop_size) is str else str(pop_size)

    def run(self, population):
        self.gen_number = 0

        return population

    def check_gen_limit(self):
        ret_val = False if self.gen_number < self.gen_limit else True
        self.gen_number += 1
        return ret_val

    def __repr__(self):
        ret_val = "SimpleInitPhase. "
        ret_val += "Generation limit={} ".format(self.gen_limit)
        ret_val += "Population Size={}".format(self.pop_size)
        return ret_val


class SimpleEvolutionDocumentationPhase(EvoPhase):
    def __init__(self, out_file_path):
        """
        This is a phase deseigned to create a textual documentation of an Evolution object
        and write it down in a file.
        :param out_file_path: This is the path of the file to which the phase
                will write the textual documentation
        """
        self.out_file_path = out_file_path
        self.evolution = None  # right now there's no Evolution object

    def run(self, population):

        if self.out_file_path is not None:
            if self.evolution is not None:
                with open(self.out_file_path, 'w') as f:
                    doc_list = self.evolution.documentation_list()
                    fixed_list = SimpleEvolutionDocumentationPhase.fix_list(doc_list, 0)

                    f.write(''.join(fixed_list))

        self.evolution = None  # Don't write this evolution again unless it is set again

        return population

    @staticmethod
    def fix_list(doc_list, depth):
        """
        Recursive function that fixes documentation list with tabs and newlines for output to file

        :param doc_list: A (partial) documentation list from an Evolution object
        :param depth: Depth in the list we are in (initially 0. we add depth tabs before each string)
        :return:
        """
        ret_val = []
        for idx, itm in enumerate(doc_list):
            if type(itm) not in [list, str]:
                raise TypeError("Expected type list or str in parameter doc_list[{}] not type {}"
                                .format(idx, type(itm)))
            elif type(itm) is str:
                ret_val.append(depth * '\t' + itm + '\n')
                print(depth * '\t' + itm)
            else:  # type(doc_list) is list
                ret_val += SimpleEvolutionDocumentationPhase.fix_list(itm, depth + 1)

        return ret_val

    def set_evolution(self, evo: Evolution):
        self.evolution = evo

    def __repr__(self):
        return "SimpleEvolutionDocumentationPhase. Out File = {}".format(self.out_file_path)


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
