from ipywidgets import interactive
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import csv , warnings
import ipywidgets as widgets
from ipywidgets import HBox
import random
import operator
import pandas as pd

def I_calc_cos2(x , c1 , c2 , c3) :
    Power = []
    c2_rad = np.array(c2)*np.pi/180 #convert to radians as numpy takes radians    
    for item in x :
        I = 0
        for i in range(min(len(c1),2)) :
            I_temp = 0 
            I_temp = c1[i]*(np.cos(abs(item) - c2_rad[i])**c3[i])
            I = I + I_temp
            
        if len(c1) == 3 :
            I_temp = 0 
            I_temp = c1[2]*(np.cos(abs(item) - c2_rad[2])**c3[2])
            I = I - I_temp            
            
        Power.append(I)
        
    return Power

def RMSE(absError , yData) : 
    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    
    return RMSE

class Params : 
    
    def __init__(self , c1 , c2 , c3) :
        self.c1 = c1 
        self.c2 = c2
        self.c3 = c3
        
    def distance(self) :
        profile = I_calc_cos2(x_axis_rad , self.c1 , self.c2 , self.c3)
        
        absError = abs(np.array(bprofile) - np.array(profile))
        distance = RMSE(absError , bprofile)
        
        return distance
    
    def __repr__(self):
        return "(" + str(self.c1) + "," + str(self.c2) +  "," + str(self.c3) + ")"

class Fitness :
    def __init__(self , profile) :
        self.profile = profile
        self.distance = 0
        self.fitness = 0.0     
        
    def profiledistance(self) :
        if self.distance == 0 :
            beam_profile = self.profile
            pathdistance = beam_profile.distance()
            
        self.distance = pathdistance
        
        return self.distance
       
    def profilefitness(self) :
        if self.fitness == 0 :
            self.fitness = 1 / float(self.profiledistance())
            
        return self.fitness

def initialPopulation(popSize):
    population = []

    for i in range(0, popSize):
        population.append(Params(c1= [1, float(random.random()) , float(random.random()) ] , 
                                 c2= [float(random.random()*1), float(random.random() * 90) , int(random.random() * 90)] ,
                                 c3= [int(random.random()*10) , int(random.random()*200) , int(random.random()*200) ]))
    return population

def rankParams(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).profilefitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []

    geneA = random.randint(1,3)
    if geneA == 1 :
        child.append(Params(parent1.c1 , parent2.c2 , parent2.c3))
    elif geneA == 2 :
        child.append(Params(parent2.c1 , parent1.c2 , parent2.c3))
    else :
        child.append(Params(parent2.c1 , parent2.c2 , parent1.c3))
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child[0])
    return children

def mutate(individual, mutationRate):

    if(random.random() < mutationRate):
        chance = random.randint(1,3)
        if chance == 1 :
            individual.c1 = [1 , float(random.random()), float(random.random())] 
        elif chance == 2 :
            individual.c2 = [float(random.random()*5), int(random.random() * 90) , int(random.random() * 90)]
        else :
            individual.c3 = [int(random.random()*10) , int(random.random()*200) ,int(random.random()*200) ]
            
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankParams(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize)
    progress = []
    err = 1 / rankParams(pop)[0][1]
    progress.append(err)
    print("Initial Error: " + str(err*100)[:5] + " %")
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankParams(pop)[0][1])
    
    print("Final Error: " + str((1 / rankParams(pop)[0][1])*100)[:5] + " %")
    bestprofileIndex = rankParams(pop)[0][0]
    bestprofile = pop[bestprofileIndex]
    return bestprofile , progress

def model_param(ParameterTuple) :
    c1 = ParameterTuple.c1
    c2 = ParameterTuple.c2
    c3 = ParameterTuple.c3
        
    return c1 , c2 , c3 

def GA_plot(final , progress) :
    c1 , c2 ,c3 = model_param(final)
    ModelPrediction = I_calc_cos2(x_axis_rad , c1 , c2 , c3 )

    print("Model Variables")
    print("\t   c1 \t\t   c2 \t\t   c3")
    for i in range(len(c1)) :
        print("%i. \t %1.3e \t %1.3e \t %1.3e " % (i+1 , c1[i] , c2[i] , c3[i]))

    plt.figure(figsize=(20,10))
    plt.subplot(1,2,1)
    plt.plot(x_axis , ModelPrediction , label = 'Model')
    plt.plot(x_axis , bprofile , label = "Target")
    plt.xticks(np.arange(-90 , 100 , step = 15))
    plt.yticks(np.arange(0,1.1 , step = 0.1))
    plt.title("Radiation Pattern for %s LED" % datasheet[:-4])
    plt.xlabel("Radation Angle $(^\circ)$")
    plt.ylabel("Nominal Power")
    plt.legend()
    plt.grid()

    plt.subplot(1,2,2)
    plt.plot(progress)
    plt.title("Genetic Algorithm Progress")
    plt.ylabel('RMSE')
    plt.xlabel('Generation')

    plt.show()

