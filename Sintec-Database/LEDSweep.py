import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Gaussian_Power_Model
import Cosine_Power_Model



filename = r'LED'
noofsweeps = 5
boxcar = 6
filename = r'680nm_1125-1084-ND_sweeps'+str(noofsweeps)+ '_boxcar'+ str(boxcar)+'_.xlsx'
dir = '1'

ser = serial.Serial("COM10", 9600, timeout = 5)

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


avg = np.mean(data, axis = 1)
ax2.plot(angle, avg)
ax2.set_title("Average of Sweeps")
ax2.set_xlabel ("Angle (degrees)")


df= pd.DataFrame(avg)
filt = df.rolling(boxcar, min_periods=1).mean()
background = filt.min()
shifted = (filt-background)
peak = shifted.max()
normalised = (shifted/peak)

export['Response (normalised)'] = normalised

fig, fig2 = plt.subplots()
fig2.plot(angle, normalised)
fig2.set_title("LED Response Normalised")
fig2.set_xlabel("Angle (degrees)")

export_excel = export.to_excel (filename, index = False, header=True) #Don't forget to add '.xlsx' at the end of the path

bound_gauss = [[.1 , [0 , 1] , [0 ,90] , [0 , 90]] , [.2 ,[0,.2] , [0 , 90] , [0 , 90]] , [.2, [0 , 0.2] , [0 ,90] , [0 , 90]] ]

Power_g , Error_g , Param_g = Gaussian_Power_Model.model_fit(angle , normalized , .02 , bound_gauss)
Gaussian_Power_Model.model_plot(Param_g , x_axis , y_axis)

bound_cos = [[.01 , [0 , 1] , [0 ,0] , [0 , 10]] , [.05,[0,.2] , [45 , 90] , [0 , 200]] , [.05, [0 , 0.2] , [0 ,45] , [0 , 200]] , [.015,[0 , 0.2] , [0 ,90] , [0 , 200]]]

Power_c , Error_c , Param_c = Cosine_Power_Model.model_fit(angle , normalized , .02 , bound_cos)
Cosine_Power_Model.model_plot(Param_c , x_axis , y_axis)

Param , model = Gaussian_Power_Model.model_choice(Param_c , Power_c , Param_g , Power_g , y_axis)




