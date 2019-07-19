#This funtion will take the list of data, find where the peaks/maximums are, 
#and then center the data by averaging the leftmost and rightmost peak index 
#values.

def centerdata(originalDataArray, totalIndexLength):
    
    import numpy as np
    import numpy
    import peakutils
    from peakutils.plot import plot as pplot
    from matplotlib import pyplot
    
    #funtion to find the maximum points in the array and display graph
    angle = np.arange(-89.55, 90, 0.45)
    indexes = peakutils.indexes(originalDataArray, thres=0.8, min_dist=10)
    print("Peak Indices/Index: ",indexes)
    pyplot.figure(figsize=(6,4))
    pplot(angle, originalDataArray, indexes)
    pyplot.title('Peaks Located')
    
    #This code will modify the indices to center at 0
    avgIndex = (indexes[0] + indexes[-1])/2
    maxIndex = int(avgIndex)
    
    if maxIndex>200:
      shiftValue =  maxIndex - 200 
      newnormalised = np.array(originalDataArray)
     
      for k in range (0, totalIndexLength-1):
          if k>=(totalIndexLength-1-shiftValue) :
              newnormalised[k] = 0
          else:
              newnormalised[k] = originalDataArray[k+shiftValue] 
    
    else:
      shiftValue = 200 - maxIndex 
      newnormalised = np.array(originalDataArray)
    
      for k in range (0, totalIndexLength-1):
          if k<=shiftValue :
              newnormalised[k] = 0
          else:
              newnormalised[k] = originalDataArray[k-shiftValue] 
    
    return newnormalised

#The output is an array of the modified values. When graphed
#it should all be centered at zero