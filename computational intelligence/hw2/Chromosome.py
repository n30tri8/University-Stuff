from random import randint
from math import pow, sqrt
from statistics import pstdev
from file_handler import read_from_file_d1

dataset1 = read_from_file_d1()

class Chromosome:
    minVal = 0
    maxVal = 9
    chromosome_length = 6
    #genes = []
    #score = 0
    #x = 0
    #y = 0

    def __init__(self, genes=None):
        self.genes = []
        self.score = 0
        self.x = 0.0
        self.y = 0.0
        if genes is None:
            for i in range(self.chromosome_length):
                self.genes.append(randint(self.minVal, self.maxVal))
        else:
            self.genes = genes

    def calc_vector_components(self):
        i = 0
        for g in self.genes:
            if i == 0:
                pass
            else:
                self.x += g * pow(10, -1*i)
            i += 1
        if self.genes[0] > 5:
            self.x = self.x*-1

        self.y = sqrt(1 - self.x**2)

    def project_points(self, ds):
        z_arr = []
        for p in ds:
            z_arr.append((self.x*p[0]) + (self.y*p[1]))
        return z_arr

    def evaluate(self):
        """
        Update Score Field Here
        """
        self.calc_vector_components()
        z_arr = self.project_points(dataset1)
        self.score = pstdev(z_arr)

if __name__ == "__main__":
    chor = Chromosome()
    print(chor.genes)
    chor.calc_vector_components()
    print(chor.x)
    print(chor.y)
    chor.evaluate()
    print(chor.score)
    print('--------------')
    chor = Chromosome()
    print(chor.genes)
    chor.calc_vector_components()
    print(chor.x)
    print(chor.y)
    chor.evaluate()
    print(chor.score)
