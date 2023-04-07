import os
import warnings
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from plot import *
import time
import math

from GeneticAlg import GA

warnings.simplefilter('ignore')


def get_file_path(name):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'ALL_tsp', name + ".tsp")
    return file_path

def distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    return math.sqrt((x1 - x2) **2 + (y1 - y2) **2)

def get_mat_from_array(array):
    mat = [[0 for i in range(len(array))] for j in range(len(array))]

    for i in range(len(array)):
       for j in range(len(array)):
            p1 = [array[i][0], array[i][1]]
            p2 = [array[j][0], array[j][1]]
            mat[i][j] = distance(p1, p2)
    return mat

def read_graph_from_file(file_name):
    file_path = get_file_path(file_name)

    # Open input file
    infile = open(file_path, 'r')

    # Read instance header
    Name = infile.readline().strip().split()[1] # NAME
    FileType = infile.readline().strip().split()[1] # TYPE
    Comment = infile.readline().strip().split()[1] # COMMENT
    Dimension = int(infile.readline().strip().split()[1]) # DIMENSION
    EdgeWeightType = infile.readline().strip().split()[1] # EDGE_WEIGHT_TYPE
    infile.readline()

    # Read node list
    nodeCoords = []
    for i in range(0, int(Dimension)):
        x,y = infile.readline().strip().split()[1:]
        nodeCoords.append([float(x), float(y)])

    mat = get_mat_from_array(nodeCoords)

    # Close input file
    infile.close()

    graph = { 'Name': Name, 'FileType': FileType, 'Comment': Comment, 'Dimension': Dimension, 
             'EdgeWeightType': EdgeWeightType, 'mat': mat }

    return graph


def plot_network(G, communities):
    np.random.seed(333)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(16, 16))
    nx.draw_networkx_nodes(G, pos, node_size=800, cmap=plt.cm.RdYlBu, node_color=communities)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()


def fitness_func(path, graph):
    mat = graph['mat']
    sum = 0
    for i in range(len(path) - 1):
        sum += mat[path[i]][path[i+1]]
    return sum

def run_ga(network, ga_param, fitness_func, file):
    ga = GA(fitness_func, ga_param)
    ga.initialisation(network)
    ga.evaluation(network)

    # Plotting params
    plotParam = {'file': file, 'allBestFitnesses' : [], 'allWorstFitnesses' : [], 'allAvgFitnesses' : [], 'generations': [], 'bestChromosome': []}

    plotParam['allBestFitnesses'].append(ga.best_chromosome().fitness)
    plotParam['allWorstFitnesses'].append(ga.worstChromosome().fitness)
    plotParam['allAvgFitnesses'].append(ga.averageFitness())
    plotParam['generations'].append(0)

    best_crom = ga.best_chromosome()
    best_chromosomes = []

    for generation in range(ga_param['noGen']):
        ga.one_generation(network)

        current_best = ga.best_chromosome()
        plotParam['allBestFitnesses'].append(ga.best_chromosome().fitness)
        plotParam['allWorstFitnesses'].append(ga.worstChromosome().fitness)
        plotParam['allAvgFitnesses'].append(ga.averageFitness())
        plotParam['generations'].append(generation)
        # print(str(generation + 1) + ' Current best: ' + ' \nFitness: '
        #       + str(current_best.fitness))

        if current_best.fitness < best_crom.fitness:
            best_crom = current_best
            best_chromosomes = []
            best_chromosomes.append(best_crom)
        elif current_best.fitness == best_crom.fitness:
            best_chromosomes.append(best_crom)
        # print(best_chromosomes)

    plotParam['bestChromosome'] = best_chromosomes

    return plotParam


if __name__ == '__main__':
    crtDir = os.getcwd()
    
    file = 'berlin52'

    network_ = read_graph_from_file(file)
    network_aux = network_.copy()

    ga_params = {'popSize': 50, 'noGen': 100, 'mutFactor': 30}

    stTime = time.time()
    plotParam = run_ga(network_aux, ga_params, fitness_func, file)
    timeSpent = time.time() - stTime
    print("--- TOTAL %s seconds ---" %(timeSpent))

    for bestc in plotParam['bestChromosome']:
        print(bestc)

    printAndSavePlot(plotParam, timeSpent)