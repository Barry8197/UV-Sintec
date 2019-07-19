import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import numpy
import centering


filename = r'LED'
noofsweeps = 1
boxcar = 10
filename = r'shifting test'+str(noofsweeps)+ '_boxcar'+ str(boxcar)+'_.xlsx'
dir = '1'
reset = '3'
lengthIndex=400
ser = serial.Serial("COM3", 9600, timeout = 5)
time.sleep(3)
ser.write(str.encode(reset))
  
try:
    line = ser.readline()

    data = np.zeros([2*noofsweeps, lengthIndex-1])
    for j in range (0, 2*noofsweeps):
        ser.write(str.encode(dir))
        time.sleep(3)

        line = ser.readline()
       # print(line)

        for i in range (0,lengthIndex-1):
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
peak1 = shifted.max()
normalised = (shifted/peak1)
normalised = np.array(normalised[0])

#function that centers the data at 0
newnormalised = centering.centerdata(normalised, lengthIndex)

#graphs the centered data
result = np.where(newnormalised == np.amax(newnormalised))
fig, fig2 = plt.subplots()
fig2.plot(angle, newnormalised)
fig2.set_title("LED Response Normalised (Centered)")
fig2.set_xlabel("Angle (degrees)")
export_excel = export.to_excel (filename, index = False, header=True)