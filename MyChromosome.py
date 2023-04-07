import random

import networkx as nx


class MyChromosome:
    def __init__(self):
        self.__fitness = 0.0
        self.__representation = []

    @property
    def representation(self):
        return self.__representation

    @property
    def fitness(self):
        return self.__fitness

    @representation.setter
    def representation(self, chromosome_rep):
        self.__representation = chromosome_rep

    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    # def normalize_rep(self):
    #     unique_nums = list(dict.fromkeys(self.__representation))
    #     self.__representation = [unique_nums.index(value) + 1 for value in self.__representation]

    def crossover(self, other):
        offspring1 = MyChromosome()
        offspring2 = MyChromosome()

        slice_start = random.randint(0, len(self.__representation))
        slice_end = random.randint(slice_start, len(self.__representation))
        
        offspring1.__representation = [-1 for i in range(len(self.__representation))]
        offspring2.__representation = [-1 for i in range(len(self.__representation))]

        for i in range(slice_start, slice_end):
            offspring1.__representation[i] = other.__representation[i]
            offspring2.__representation[i] = self.__representation[i]
        
        x,y = 0,0
        for i in range(0, slice_start):
            while self.__representation[x] in offspring1.__representation:
                x += 1

            while other.__representation[y] in offspring2.__representation:
                y += 1
            
            offspring1.__representation[i] = self.__representation[x]
            offspring2.__representation[i] = other.__representation[y]

        for i in range(slice_end, len(self.__representation)):
            while self.__representation[x] in offspring1.__representation:
                    x += 1

            while other.__representation[y] in offspring2.__representation:
                y += 1
            
            offspring1.__representation[i] = self.__representation[x]
            offspring2.__representation[i] = other.__representation[y]

        # for i in range(1, len(self.__representation) - 1):
        #     while offspring1[i] == -1:
        #         if parent2.__representation[parent2_index] not in offspring1:
        #             offspring1[i] = parent2.__representation[parent2_index]
        #         parent2_index += 1

        #     while offspring2[i] == -1:
        #         if self.__representation[parent1_index] not in offspring2:
        #             offspring2[i] = self.__representation[parent1_index]
        #         parent1_index += 1

        return [offspring1, offspring2]
    
    # def order_crossover(self, parent2):
    #         # Select a random slice from parent 1
    #     slice_start = random.randint(1, len(self.__representation) - 2)
    #     slice_end = random.randint(slice_start, len(self.__representation) - 2)

    #     # Initialize offspring with slice
    #     offspring1 = [-1] * len(self.__representation)
    #     offspring1[slice_start:slice_end] = self.__representation[slice_start:slice_end]
    #     offspring1[0] = self.__representation[0]
    #     offspring1[-1] = self.__representation[-1]

    #     offspring2 = [-1] * len(self.__representation)
    #     offspring2[slice_start:slice_end] = parent2.__representation[slice_start:slice_end]
    #     offspring2[0] = self.__representation[0]
    #     offspring2[-1] = self.__representation[-1]

    #     # Fill in remaining cities from parent 2
    #     parent2_index = 1
    #     parent1_index = 1
    #     for i in range(1, len(self.__representation) - 1):
    #         while offspring1[i] == -1:
    #             if parent2.__representation[parent2_index] not in offspring1:
    #                 offspring1[i] = parent2.__representation[parent2_index]
    #             parent2_index += 1

    #         while offspring2[i] == -1:
    #             if self.__representation[parent1_index] not in offspring2:
    #                 offspring2[i] = self.__representation[parent1_index]
    #             parent1_index += 1

    #     off1 = MyChromosome()
    #     off2 = MyChromosome()
    #     off1.__representation = offspring1 
    #     off2.__representation = offspring2

    #     return off1, off2

    def mutation(self, mutation_rate):
        rnd_chance = random.randint(0, 100)
        if rnd_chance < mutation_rate:
            poz_1 = random.randint(0, len(self.__representation) - 1)
            poz_2 = random.randint(0, len(self.__representation) - 1)
            self.__representation[poz_1], self.__representation[poz_2] =\
                self.__representation[poz_2], self.__representation[poz_1]

    def init_representation(self, network):
        size = network['Dimension']
        self.__representation = [i for i in range(size)]
        random.shuffle(self.__representation)


    def __str__(self):
        return '\nChromosome: ' + str(self.__representation) + ' --- fit: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__representation == c.__repres and self.__fitness == c.__fitness