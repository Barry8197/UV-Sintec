# Spectral Line Shaping

## Spectral_Line_Shape.py

Textfile_read() - reads the textfile of a given filename and returns the normalized intensisty as well as the x_axis  
center_peak() - finds the peak wavelength and crops the intenisty and x_axis to be uniform around this peak  
find_nearest() - finds the location of the closest element in a array to a given value 
fwhm_finder() - finds the full width half max for the specific file intensity and x axis  
Lorentz() - calculates the Lorentz value for the given file  
Gaussian() - calculates the Gaussian value for the given file  
spectral_line_fit() - finds the best weighting between the Gaussian and Lorentz for the given file  

## Spectral_Line_Fit.ipynb

Takes every ".txt" file in the local directory and finds the optimum weighting for each LED wavelength measurement
