import numpy as np
import os

def Textfile_read(filename) :

    f = open(filename , 'r')
    data = f.read()

    intensity = []
    x_axis = []
    for item in data.split('\n')[:-1] :
        intensity_temp , x_axis_temp = item.split(' ')
        x_axis.append(float(intensity_temp))
        intensity.append(float(x_axis_temp))

    intensity_normalized = np.array(intensity)/max(intensity)
    
    return intensity_normalized , x_axis

def center_peak(x_axis , intensity) :
    intensity = list(intensity)
    peak_orig = intensity.index(max(intensity))
    x_axis_cropped = x_axis[peak_orig - 300 : peak_orig + 300]
    intensity_cropped = intensity[peak_orig - 300 : peak_orig + 300]
    peak = intensity_cropped.index(max(intensity_cropped))
    
    return x_axis_cropped , intensity_cropped  , peak

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def fwhm_finder(x_axis_cropped , intensity_cropped , peak) :
    array1 = intensity_cropped[:peak]
    array2 = intensity_cropped[peak:]
    lidx = find_nearest(array1 , 0.5)
    ridx = find_nearest(array2 , 0.5) + peak
    fwhm = x_axis_cropped[ridx] - x_axis_cropped[lidx]
    
    return fwhm

def Lorentz(x_axis) :
    x_axis = np.array(x_axis)
    Lorentz = 1/(1 + (x_axis**2))
    
    return Lorentz

def Gaussian(x) :
    x = np.array(x)
    Gauss = np.exp(-1*np.log(2)*(x**2))
    
    return Gauss

def spectral_line_fit(x_axis_cropped , intensity_cropped , peak) :
    p_0 = x_axis_cropped[peak]
    w = fwhm_finder(x_axis_cropped , intensity_cropped , peak)
    x = (p_0 - np.array(x_axis_cropped))/(w/2)
    n = np.linspace(0 , 1 , 101)
    LSE = []
    for item in n :
        Voigt = item*Gaussian(x) + (1-item)*Lorentz(x)
        SSE = np.sum(((np.array(intensity_cropped - Voigt)**2)))
        RMSE = np.sqrt(SSE / len(intensity_cropped))
        LSE.append([RMSE , item])
        
    return min(LSE) , x




    
    