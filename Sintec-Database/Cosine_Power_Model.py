import numpy as np
import matplotlib.pyplot as plt
import csv , warnings


def I_calc_cos(x , c1 ,c2 ,c3) :
    Power = []
    c2_rad = c2*np.pi/180 #convert to radians as numpy takes radians
    for item in x :      
        I = 0
        I = c1*(abs(np.cos(abs(item) - c2_rad))**c3)  #Perform Calculation for each angle
        Power.append(I)
            
    return Power

def sumOfSquaredError(xData , yData , c1 , c2 , c3):
    warnings.filterwarnings("ignore") # do not print warnings by genetic algorithm
    val = I_calc_cos(xData, c1 ,c2 ,c3) #Model Prediction
    
    return np.sum((np.array(yData) - np.array(val)) ** 2.0)

def Least_Square_Error(xData , yData , c1 , c2 , c3) :
    LSE = []
    for item1 in c1 :
        for item2 in c2 : 
            for item3 in c3 :
                SQE = sumOfSquaredError(xData , yData , item1 , item2 , item3)
                LSE.append([SQE , item1 , item2 , item3])
                
    return min(LSE)  

def Linear_Reg(accuracy , xData , yData , bound_c1 , bound_c2 , bound_c3) :
    RMSE = 1
    count = 1
    xData_rad = []
    minc1 , maxc1 = bound_c1
    minc2 , maxc2 = bound_c2
    minc3 , maxc3 = bound_c3
    
    for item in xData :
        xData_rad.append(item*np.pi/180)
        
    while RMSE > accuracy :
        """setting the boundaries within which the model will search for the LSE"""
        c1 = np.linspace(minc1 , maxc1 , 10)
        c2 = np.linspace(minc2 , maxc2 , 10)
        c3 = np.linspace(minc3 , maxc3 , 10)
        param = Least_Square_Error(xData_rad , yData , c1 , c2 , c3) #returns the optimal parameters
        absError = np.array(yData) - np.array(I_calc_cos(xData_rad , param[1] , param[2] , param[3]))

        SE = np.square(absError) # squared errors
        MSE = np.mean(SE) # mean squared errors
        RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
        Rsquared = 1.0 - (np.var(absError) / np.var(yData))
        
        """Resetting the boundaries based on initial guess"""
        minc1 , maxc1 = [max(0 , param[1]-(.1/count)) , min(1 , param[1]+(.1/count))] 
        minc2 , maxc2 = [max(0 , param[2]-(10/count)) , min(90 , param[2]+(10/count))]
        minc3 , maxc3 = [max(0 , param[3]-(5/count))  , min(200 , param[3]+(5/count))]
        
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
            
        I = I_calc_cos(x_axis_rad , param_temp[1] , param_temp[2] , param_temp[3])
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
    c1 = []
    c2 = []
    c3 = []
    for item in ParameterTuple :
        c1.append(item[0])
        c2.append(item[1])
        c3.append(item[2])
        
    return c1 , c2 , c3 

def I_calc_cos2(x , c1 , c2 , c3) :
    Power = []
    c2_rad = np.array(c2)*np.pi/180 #convert to radians as numpy takes radians    
    for item in x :
        I = 0
        for i in range(min(len(c1),3)) :
            I_temp = 0 
            I_temp = c1[i]*(np.cos(abs(item) - c2_rad[i])**c3[i])
            I = I + I_temp
            
        if len(c1) == 4 :
            I_temp = 0 
            I_temp = c1[3]*(np.cos(abs(item) - c2_rad[3])**c3[3])
            I = I - I_temp            
            
        Power.append(I)
        
    return Power

def model_plot(Param , x_axis , y_axis) :
    x_axis_rad = []
    for item in x_axis :
        x_axis_rad.append(item*np.pi/180)
    angle = np.linspace(-90 , 90 , 181*10)
    theta = angle*np.pi/180    
    c1 , c2 ,c3 = model_param(Param)
    ModelPrediction = I_calc_cos2(theta , c1 , c2 , c3 )

    print("Model Variables")
    print("\t   c1 \t\t   c2 \t\t   c3")
    for i in range(len(c1)) :
        print("%i. \t %1.3e \t %1.3e \t %1.3e " % (i+1 , c1[i] , c2[i] , c3[i]))

    plt.figure(figsize= (10,10))
    plt.plot(angle , ModelPrediction , label = "Model")
    plt.plot(x_axis , y_axis , label = "Target")
    plt.xticks(np.arange(-90 , 100 , step = 10))
    plt.yticks(np.arange(0,1.1 , step = 0.1))
    plt.title("Radiation Pattern")
    plt.xlabel("Radation Angle $(^\circ)$")
    plt.ylabel("Nominal Power")
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize= (20 ,10 ))
    plt.polar(theta , ModelPrediction)
    plt.polar(x_axis_rad , y_axis)
    plt.xlim(-np.pi/2 , np.pi/2)
    plt.show()
    
    
def model_choice(Param_c , Power_c , Param_g , Power_g , y_axis) :
    absError_c = np.array(Power_c) - np.array(y_axis)
    absError_g = np.array(Power_g) - np.array(y_axis)
    RMSE_c = RMSE(absError_c , y_axis)
    RMSE_g = RMSE(absError_g , y_axis)
    if RMSE_c < RMSE_g :
        Param = Param_c
        model = "Cosine Power Model"
    else :
        Param = Param_g
        model = "Gaussian Power Model"
        
    return Param , model