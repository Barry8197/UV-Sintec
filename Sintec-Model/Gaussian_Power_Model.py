import numpy as np
import matplotlib.pyplot as plt
import csv , warnings

def I_calc_gauss(x , g1, g2 , g3) :
    Power = []
    g2_rad = g2*np.pi/180
    g3_rad = g3*np.pi/180
    for item in  x:
        Power.append(g1*np.exp(-np.log(2)*((abs(item)-g2_rad)/g3_rad)**2))
    
    return Power

def sumOfSquaredError(xData , yData , g1 , g2 , g3):
    warnings.filterwarnings("ignore") # do not print warnings by genetic algorithm
    val = I_calc_gauss(xData, g1 ,g2 ,g3) #Model Prediction
    
    return np.sum((np.array(yData) - np.array(val)) ** 2.0)

def Least_Square_Error(xData , yData , g1 , g2 , g3) :
    LSE = []
    for item1 in g1 :
        for item2 in g2 : 
            for item3 in g3 :
                SQE = sumOfSquaredError(xData , yData , item1 , item2 , item3)
                LSE.append([SQE , item1 , item2 , item3])
                
    return min(LSE)     


def Linear_Reg(accuracy , xData , yData , bound_g1 , bound_g2 , bound_g3) :
    RMSE = 1
    count = 1
    xData_rad = []
    ming1 , maxg1 = bound_g1
    ming2 , maxg2 = bound_g2
    ming3 , maxg3 = bound_g3
    
    for item in xData :
        xData_rad.append(item*np.pi/180)
        
    while RMSE > accuracy :
        """setting the boundaries within which the model will search for the LSE"""
        g1 = np.linspace(ming1 , maxg1 , 10)
        g2 = np.linspace(ming2 , maxg2 , 10)
        g3 = np.linspace(ming3 , maxg3 , 10)
        param = Least_Square_Error(xData_rad , yData , g1 , g2 , g3) #returns the optimal parameters
        absError = np.array(yData) - np.array(I_calc_gauss(xData_rad , param[1] , param[2] , param[3]))

        SE = np.square(absError) # squared errors
        MSE = np.mean(SE) # mean squared errors
        RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
        Rsquared = 1.0 - (np.var(absError) / np.var(yData))
        
        """Resetting the boundaries based on initial guess"""
        ming1 , maxg1 = [max(0 , param[1]-(.1/count)) , min(1.5 , param[1]+(.1/count))] 
        ming2 , maxg2 = [max(0 , param[2]-(10/count)) , min(90 , param[2]+(10/count))]
        ming3 , maxg3 = [max(0 , param[3]-(10/count)) , min(90 , param[3]+(10/count))]
    
        if count == 10 :
            break
        else :
            count = count + 1
     
    return param , absError


def RMSE(absError , yData) : 
    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    Rsquared = 1.0 - (np.var(absError) / np.var(yData))    
    
    print('RMSE:', RMSE)
    print('R-squared:', Rsquared)
    
    print()
    
    return RMSE

def model_fit(x_axis , y_axis , accuracy , bound) :
    x_axis_rad = []    
    for item in x_axis :
        x_axis_rad.append(item*np.pi/180)
        
    loop = 0
    per_error = 1
    param = []
    Error = []
    Power = []
    y_Data = y_axis
        
    while per_error > accuracy :
        if loop == len(bound) :
            print("Cannot achieve desired accuracy given boundaries specified")
            print("Either increase length of boundary specification or decrease desired accuracy")
            break
        Power_temp = []
        param_temp = []
        Error_temp = []
        I = []
        
        if loop == 3 :
            param_temp , Error_temp = Linear_Reg(bound[loop][0] , x_axis , abs(y_Data) , bound[loop][1] , bound[loop][2] , bound[loop][3])
        else :
            param_temp , Error_temp = Linear_Reg(bound[loop][0] , x_axis , y_Data , bound[loop][1] , bound[loop][2] , bound[loop][3])
            
        I = I_calc_gauss(x_axis_rad , param_temp[1] , param_temp[2] , param_temp[3])
        param.append(param_temp[1:])
        Error.append(Error_temp)
        
        Power_temp = Power
        Power = []
        if loop == 0 :
            Power = I
        elif loop == 3 :
            for i in range(len(I)) :
                Power.append(Power_temp[i] - I[i])            
        else :
            for i in range(len(I)) :
                Power.append(I[i] + Power_temp[i])

        absError = np.array(Power) - np.array(y_axis)
        per_error = RMSE(absError , y_axis)

        y_Data = Error[loop]        
        loop = loop + 1
        
    return Power , Error , param

def model_param(ParameterTuple) :
    g1 = []
    g2 = []
    g3 = []
    for item in ParameterTuple :
        g1.append(item[0])
        g2.append(item[1])
        g3.append(item[2])
        
    return g1 , g2 , g3 

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
