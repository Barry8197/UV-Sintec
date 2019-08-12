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

def I_calc_gauss2(x , g1 , g2 , g3) :
    Power = []
    g2_rad = np.array(g2)*np.pi/180 #convert to radians as numpy takes radians
    g3_rad = np.array(g3)*np.pi/180 #convert to radians as numpy takes radians
    for item in x :
        I = 0
        for i in range(min(len(g1),3)) :
            I_temp = 0 
            I_temp = g1[i]*np.exp(-np.log(2)*((abs(item)-g2_rad[i])/g3_rad[i])**2)
            I = I + I_temp
            
        if len(g1) == 4 :
            I_temp = 0 
            I_temp = g1[3]*np.exp(-np.log(2)*((abs(item)-g2_rad[3])/g3_rad[3])**2)
            I = I - I_temp            
            
        Power.append(I)
        
    return Power

def RMSE(absError , yData) : 
    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    
    return RMSE

class Params : 
    
    def __init__(self , g1 , g2 , g3) :
        self.g1 = g1 
        self.g2 = g2
        self.g3 = g3
        
    def distance(self) :
        profile = I_calc_gauss2(x_axis_rad , self.g1 , self.g2 , self.g3)
        
        absError = abs(np.array(bprofile) - np.array(profile))
        distance = RMSE(absError , bprofile)
        
        return distance
    
    def __repr__(self):
        return "(" + str(self.g1) + "," + str(self.g2) +  "," + str(self.g3) + ")"

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
        population.append(Params(g1= [random.uniform(0.5 , 1) , random.uniform(0 , 0.5) , random.uniform(0 , 0.5) ] , 
                                 g2= [random.randint(0,90) , random.randint(0,90) , random.randint(0,90)] ,
                                 g3= [random.randint(1,90) , random.randint(1,90) , random.randint(1,90)]))
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
        child.append(Params(parent1.g1 , parent2.g2 , parent2.g3))
    elif geneA == 2 :
        child.append(Params(parent2.g1 , parent1.g2 , parent2.g3))
    else :
        child.append(Params(parent2.g1 , parent2.g2 , parent1.g3))
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
            individual.g1 = [random.uniform(0.5 , 1)  , random.uniform(0 , 0.5), random.uniform(0 , 0.5)] 
        elif chance == 2 :
            individual.g2 = [random.randint(0,90) , random.randint(0,90) , random.randint(0,90)]
        else :
            individual.g3 = [random.randint(1,90) , random.randint(1,90) , random.randint(1,90)]
            
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
    g1 = ParameterTuple.g1
    g2 = ParameterTuple.g2
    g3 = ParameterTuple.g3
        
    return g1 , g2 , g3 

def GA_plot(final , progress) :
    g1 , g2 , g3 = model_param(final)
    ModelPrediction = I_calc_gauss2(x_axis_rad , g1 , g2 , g3 )

    print("Model Variables")
    print("\t   g1 \t\t   g2 \t\t   g3")
    for i in range(len(g1)) :
        print("%i. \t %1.3e \t %1.3e \t %1.3e " % (i+1 , g1[i] , g2[i] , g3[i]))

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

