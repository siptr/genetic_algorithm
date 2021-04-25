# -*- coding: utf-8 -*-
"""GA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13rA9MEcDtZAT7glmHhqMRA9GVcRHghG2

author  : **Muhammad Kiko** | **Siti Inayah Putri** | **I GSA Putu Sintha Deviya**

---

# Import Library
Random dan Math.
"""

import random
import math

"""# Inisialisasi Parameter."""

#PARAMETER
population_size = 40
bb_x = -1 #batas bawah x
ba_x = 2 #batas atas x
bb_y = -1 #batas bawah y
ba_y = 1 #batas atas y
#INPUT PANJANG CHROMOSOME
gen_length = 4
chromosome_length = gen_length * 2
#INPUT CROSSOVER DAN MUTATION PROBABILITY 
cross_rate = 0.6
mutate_rate = 0.2
#INPUT FITNESS THRESHOLD
fitness_threshold = 2.47
#TOURNAMENT SIZE
tourney_size = 5

"""# Generate Population."""

def generate_chromosome(length=chromosome_length):
    return [random.randint(0,1) for x in range(length)] 

def first_generation(popsize = population_size):
    population = []
    for i in range(popsize):
        population.append(generate_chromosome())
    return population

"""# Decode Chromosome."""

def todec(x):
    return int("".join(map(str,x)),2)
def decode(chromosome):
    limx = ba_x-(bb_x)
    limb = ba_y-(bb_y)
    c_half = int(len(chromosome)/2)
    x1 = todec(chromosome[:c_half])
    y1 = todec(chromosome[c_half:])
    sum_gen =  2 ** (len(chromosome)/2)-1
    x2 = bb_x + (x1/sum_gen)*limx
    y2 = bb_y + (y1/sum_gen)*limb 
    return round(x2,2), round(y2,2)

"""# Fitness."""

def calc_Fitness(chromosome):
    x, y = decode(chromosome)
    return (math.cos(x*x)*math.sin(y*y)) + (x + y)

"""# Parent Selection Menggunakan Metode Tournament."""

def tournament(population, size = tourney_size):
    win = None
    ran_number = random.sample(range(0, len(population)-1),size)
    for i in ran_number:
        chromosome = population[i]
        if win is None or calc_Fitness(chromosome) > calc_Fitness(chromosome):
            win = chromosome
    return win

"""# Crossover Single-Point."""

def crossover(c1, c2, rate = cross_rate):
    random_rate = random.random()
    if (random_rate <= rate):
        random_point = random.randint(0, chromosome_length - 1)
        child1 = (c1[0:random_point]+c2[random_point:chromosome_length])
        child2 = (c2[0:random_point]+c1[random_point:chromosome_length])
        return child1, child2
    return c1, c2

"""# Mutation."""

def mutation(chromosome, rate = mutate_rate):
    random_rate = random.random()
    if (random_rate <= rate):
        random_idx = random.randint(0, chromosome_length-1)
        chromosome[random_idx] = 1 if (chromosome[random_idx] == 0) else 0

"""# Elitism."""

def first_elitism(population):
    best = None
    for i in range(len(population)):
        if (best == None or calc_Fitness(population[i]) > calc_Fitness(best)):
            best = population[i]
    return best

def second_elitism(population):
    best = first_elitism(population)
    best2 = None
    for i in range(len(population)):
        if (best2 == None or 
            (calc_Fitness(population[i]) > calc_Fitness(best2) and 
             calc_Fitness(population[i]) < calc_Fitness(best) and 
             population[i] != best)):
            best2 = population[i]
    return best2

"""# Change Generation."""

def change_generation(current_population):
    new_population = []
    while len(new_population) != len(current_population) - 2:
        parent1 = tournament(current_population)
        parent2 = tournament(current_population)
        while parent1 == parent2:
            parent2 = tournament(current_population)

        child1, child2 = crossover(parent1, parent2)
        mutation(child1)
        mutation(child2)
        new_population.append(child1)
        new_population.append(child2)

    new_population.append(first_elitism(current_population))
    new_population.append(second_elitism(current_population))
    return new_population

"""---

# Main Program.
"""

print("------------------------------------------------------------------------------------------")
best = []
x = first_generation()
print('Best of Generasi ke', 0, " | Chromosome :", "".join(str(j) for j in first_elitism(x)),
        " | Fitness :", round(calc_Fitness(first_elitism(x)),2),
        " | (X, Y) :", decode(first_elitism(x)))
best.append(first_elitism(x))
i = 0

while calc_Fitness(first_elitism(x)) < fitness_threshold:
    i+=1
    x = change_generation(x)
    best.append(first_elitism(x))
    print('Best of Generasi ke', i, " | Chromosome :", "".join(str(j) for j in first_elitism(x)), 
            " | Fitness :", round(calc_Fitness(first_elitism(x)),2),
        " | (X, Y) :", decode(first_elitism(x)))
print("-------------------------------------------------------------------------------------------")
print("")
print("------------- The Best of The Best -----------")
bestof = first_elitism(best)
print("Chromosome   : ", "".join(str(k)for k in bestof))
print("Fitness      : ", round(calc_Fitness(bestof),2))
print("(X, Y)       : ", decode(bestof))
print("---------------------------------------------")