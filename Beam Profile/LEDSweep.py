import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Gaussian_Power_Model
import Cosine_Power_Model
import Database_Update

wavelength = str(input("Enter Manufacturer Wavelength in nm :")).replace(" ", "")+"nm"
product_code = str(input("Enter Full Product Code:")).replace(" ", "")
noofsweeps = int(input("Enter Number of Sweeps Completed in integers:"))
boxcar = int(input("Please Enter Boxcar Value :"))
filename = wavelength + '_' + product_code + r'_sweeps'+str(noofsweeps)+ '_boxcar'+ str(boxcar)+'_.xlsx'
print("")
print("The filename is %s" % filename)
print("")
LEDAngles = np.array

for difAngle in range (0, 3):
    LEDAngle = int(input("Please Enter Angle of LED:"))
    dir = '1'
    reset ='3'
    ser = serial.Serial("COM4", 9600, timeout = 5)
    time.sleep(3)

#for j in range (0, 3):
    
    
    LEDAngle = int(input("Please Enter Angle of LED:"))
    ser.write(str.encode(reset))
    try:
        line = ser.readline()

        data = np.zeros([2*noofsweeps, 399])
        for j in range (0, 2*noofsweeps):
            ser.write(str.encode(dir))
            time.sleep(3)
            
            line = ser.readline()
            # print(line)
            
            for i in range (0,399):
                line = ser.readline()
                #  print(line)
                data[j, i] = float(line)
                
                if ((j%2)==0):
                    data[j] = np.flip(data[j])
                    
                    if(dir == '1'):
                        dir = '2'
                    elif(dir=='2'):
                        dir='1'
                            
    finally:
        ser.close()    
    
    data = np.transpose(data)
    angle = np.arange(-89.55, 90, 0.45)   
    export = pd.DataFrame()
    export['Angle'] = angle
    
    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(angle, data)
    ax1.set_title('Different Sweeps')
    ax1.set_xlabel('Angle (degrees)')
    ax1.grid()
    
    avg = np.mean(data, axis = 1)
    ax2.plot(angle, avg)
    ax2.set_title("Average of Sweeps")
    ax2.set_xlabel ("Angle (degrees)")
    ax2.grid()
    plt.show()
    
    
    df= pd.DataFrame(avg)
    filt = df.rolling(boxcar, min_periods=1).mean()
    background = filt.min()
    shifted = (filt-background)
    peak = shifted.max()
    normalised = (shifted/peak)
    fig, fig2 = plt.subplots()
    fig2.plot(angle, normalised)
    fig2.set_title("LED Response Normalised")
    fig2.set_xlabel("Angle (degrees)")
    fig2.grid()
    plt.show()
    
#export['Response (normalised)'+difAngle] = normalised



#export_excel = export.to_excel (filename, index = False, header=True) #Don't forget to add '.xlsx' at the end of the path

    normalised[difAngle] = np.array(normalised[0])  
    LEDAngles[difAngle] = LEDAngle

bound_gauss = [[.1 , [1 , 1] , [0 ,90] , [0 , 90]] , [.2 ,[0,.2] , [0 , 90] , [0 , 90]] , [.2, [0 , 0.2] , [0 ,90] , [0 , 90]] , [.2, [0 , 0.2] , [0 ,90] , [0 , 90]]]

Power_g , Error_g , Param_g = Gaussian_Power_Model.model_fit(angle , normalised[0] , .02 , bound_gauss)
Gaussian_Power_Model.model_plot(Param_g , angle , normalised[0])

bound_cos = [[.1 , [1 , 1] , [0 ,0] , [0 , 10]] , [.1,[0,.2] , [45 , 90] , [0 , 200]] , [.1, [0 , 0.2] , [0 ,45] , [0 , 200]] , [.1,[0 , 0.2] , [0 ,90] , [0 , 200]]]

Power_c , Error_c , Param_c = Cosine_Power_Model.model_fit(angle , normalised[0] , .02 , bound_cos)
Cosine_Power_Model.model_plot(Param_c , angle , normalised[0])

Param , model , RMSE = Gaussian_Power_Model.model_choice(Param_c , Power_c , Param_g , Power_g , normalised[0])

print("The optimal RMSE is %1.3f%%" % (RMSE*100)) 
add_model = str(input("Do you want to add this model to the Database (y/n) :")).replace(" ","")
check = False
while check == False :
    if add_model.lower() == "y" :
        Database_Update.write_to_database(product_code , wavelength , model , Param , RMSE , normalised[0].tolist())
        check = True
    elif add_model.lower() == "n" :
        check = True
    else :
        print("")
        print("Error please select y/n")
        check = False



