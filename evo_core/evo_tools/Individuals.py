import copy as cp
import random as r
from evo_core.Population_Containers import Individual


class VectorIndividual(Individual):
    def __init__(self, genome):
        self.genome = cp.deepcopy(genome)

    def __len__(self):
        return len(list(self.genome))

    def develop(self):
        return cp.deepcopy(self.genome)

    def self_replicate(self):
        return cp.deepcopy(self)

    # Phase tools

    def perform_uniform_plus_mutation(self, mutation_probability=None):
        if not mutation_probability:
            mutation_probability = 1.0/len(self)
            locations, new_genes = self.get_uniform_plus_mutation_stats(mutation_probability)
            self.rewrite_multiple_genes(locations, new_genes)

    def perform_swap_mutation(self, mutation_probability=1.0):
        if r.random() < mutation_probability:
            locations = r.sample(range(len(self.genome)), 2)
            self.rewrite_multiple_genes(locations, cp.deepcopy([self.genome[locations[1]], self.genome[locations[0]]]))

    def get_point_mutation_stats(self):
        length = len(self.genome)
        location = r.randrange(length)
        new_gene = self.generate_new_gene_sequence(1)
        return location, new_gene

    def get_rewrite_mutation_stats(self, min_length=1, max_length=1):
        length = len(self.genome)
        gene_length = r.randint(min_length, max_length)
        location = r.randrange(length)
        new_genes = self.generate_new_gene_sequence(gene_length)
        return location, new_genes

    def get_jump_mutation_stats(self):
        length = len(self.genome)
        source_location = r.randrange(length)
        dest_location = r.randrange(length)
        new_genes = self.generate_new_gene_sequence(1)
        return source_location, dest_location, new_genes

    def get_uniform_mutation_stats(self, probability, doubling_probability):
        length = len(self.genome)
        locations = []
        new_genes = []

        while probability < 1 and r.random() < doubling_probability:
            probability *= 2

        for i in range(length):
            if r.random() < probability:
                locations.append(i)
                new_genes.append(self.generate_new_gene_sequence(1)[0])
        return locations, new_genes

    def get_uniform_plus_mutation_stats(self, probability):
        length = len(self.genome)
        locations = []
        new_genes = []

        # geometric random variable for number of iterations on genome.
        first_iter = True
        # while rn.random() < 0.5:
        while first_iter or r.random() < 0.5:
            first_iter = False
            for i in range(length):
                if (i not in locations) and (r.random() < probability):
                    locations.append(i)
                    new_genes.append(self.generate_new_gene_sequence(1)[0])
        return locations, new_genes

    def get_random_xo_points(self, num_of_points):
        length = len(self.genome)
        points = sorted([r.randrange(length) for _ in range(num_of_points)])
        return points

    def get_uniform_xo_stats(self, probability):
        length = len(self.genome)
        locations = []
        for i in range(length):
            if r.random() < probability:
                locations.append(i)
        return locations

    def copy_paste_genes(self, location1, location2, length):
        self.genome[location2:location2 + length] = self.genome[location1:location1 + length]

    def cut_paste_genes(self, location1, location2, length):
        genes = self.genome[location1:location1 + length]
        self.genome = self.genome[:location1]+self.genome[location1+length:]
        if location2 <= location1:
            self.genome = self.genome[:location2]+genes+self.genome[location2+length:]
        elif location2 <= location1+length:
            # Do nothing.
            self.genome = self.genome[:location1]+genes+self.genome[location1+length:]
        else:  # location2 > location1+length.adjust index change in genome.
            self.genome = self.genome[:location2-length]+genes+self.genome[location2:]

    # Action tools

    def rewrite_genes(self, location, genes):
        self.genome[location:location+len(genes)] = genes
        # for i in range(len(genes)):
        #     self.genome[location + i] = genes[i]

    def rewrite_multiple_genes(self, locations, genes):
        """

        Args:
            locations: list of locations to be replaced.
            genes:  list of new genes (not a list of lists by design!)

        """
        for i in range(len(locations)):
            self.genome[locations[i]] = genes[i]

    def copy_paste_genes(self, location1, location2, length):
        self.genome[location2:location2 + length] = self.genome[location1:location1 + length]

    def cut_paste_genes(self, location1, location2, length):
        genes = self.genome[location1:location1 + length]
        self.genome = self.genome[:location1]+self.genome[location1+length:]
        if location2 <= location1:
            self.genome = self.genome[:location2]+genes+self.genome[location2+length:]
        elif location2 <= location1+length:
            # Do nothing.
            self.genome = self.genome[:location1]+genes+self.genome[location1+length:]
        else:  # location2 > location1+length.adjust index change in genome.
            self.genome = self.genome[:location2-length]+genes+self.genome[location2:]

    def rewrite_genes(self, location, genes):
        self.genome[location:location+len(genes)] = genes
        # for i in range(len(genes)):
        #     self.genome[location + i] = genes[i]

    def copy_paste_genes(self, location1, location2, length):
        self.genome[location2:location2 + length] = self.genome[location1:location1 + length]

    def cut_paste_genes(self, location1, location2, length):
        genes = self.genome[location1:location1 + length]
        self.genome = self.genome[:location1]+self.genome[location1+length:]
        if location2 <= location1:
            self.genome = self.genome[:location2]+genes+self.genome[location2+length:]
        elif location2 <= location1+length:
            # Do nothing.
            self.genome = self.genome[:location1]+genes+self.genome[location1+length:]
        else:  # location2 > location1+length.adjust index change in genome.
            self.genome = self.genome[:location2-length]+genes+self.genome[location2:]

    def rewrite_genes(self, location, genes):
        self.genome[location:location+len(genes)] = genes
        # for i in range(len(genes)):
        #     self.genome[location + i] = genes[i]


class IntVectorIndividual(VectorIndividual):
    def __init__(self, genome, min_int=0, max_int=1000000):
        super().__init__(genome)
        self.max_int = max_int
        self.min_int = min_int
        self.phenome = self.develop()

    def distance(self, other):
        """
        This function evaluates the distance between two individuals
        Args:
            other: Another individual

        Returns: Distance. i.e. number locations for witch self and other differ.
                 Returns as floating point number.

        """
        ret_val = 0.0
        ind1 = self.genome
        ind2 = other.genome

        for i in range(min(len(ind1), len(ind2))):
            if ind1[i] == ind2[i]:
                pass
            else:
                ret_val += 1.0

        ret_val += (max(len(ind1), len(ind2)) - min(len(ind1), len(ind2)))

        return ret_val

    # Phase tools

    def generate_new_gene_sequence(self, length):
        ret_val = []
        for i in range(length):
            ret_val.append(r.randrange(self.min_int, self.max_int))
        return ret_val

    # Action tools



