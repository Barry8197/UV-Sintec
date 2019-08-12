# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:18:32 2019

@author: emlon
"""

import os, csv

def interp(x, y, x1):
    '''
    Linearly interpolates the curve given by lists x and y at point x1.
    The list x must be increasing
    '''
    # Find where x crosses x1
    i = next((idx - 1 for idx, val in enumerate(x) if val > x1), len(x) - 2)
    # dx is the distance past x[i] we need to go
    dx = x1 - x[i];
    print (dx)
    # Use the slope to figure out dy, and add to y[i]
    slope = (y[i+1] - y[i]) / (x[i+1] - x[i])
    dy = slope * dx
    y1 = y[i] + dy

    return y1

if 'SpecValsFinal1.txt' in os.listdir('.'):
    specfilename = 'SpecValsFinal1.txt'
    
    with open(specfilename) as f:
        specfile = csv.reader(f)
        # Save wavelength and factor values as a dict of lists
        specdata = {
            'wavelen': [],
            'factor': [],
        }
        for row in specfile:
                specdata['wavelen'].append(float(row[0]))
                specdata['factor'].append(float(row[1]))
           # print(specdata) starts at 250nm
        
else:
    raise Exception('File SpecValsFinal1.txt not found!')

summarydata = []

# Iterate all led files

for filename in os.listdir('.'):

    # Validate all file names, make sure we're only reading LED data
    if os.path.isdir(filename):
        continue
    
    if filename == os.path.basename(__file__):
        print('Ignoring file {0}, it is me!'.format(filename))
        continue
        
    if filename == 'SpecValsFinal1.txt':
        continue

    if not filename.endswith(".txt"):
        print('Ignoring file {0}, not a .txt file'.format(filename))
        continue
        
        
    # Get led info from file name
    
    ledname = os.path.splitext(filename)[0]
    fileparts = ledname.split('-')

    # Make sure file name is correct format/length
    if not len(fileparts) == 7:
        print('Ignoring file {0}, not named in the correct format'.format(filename))
        continue
        
    print('Processing file {0}'.format(filename))

    # Get led info
    [wavelen, current, inttime, boxcaravg, nscans, bgsignal, num] = fileparts
    
    # Convert inttime to a float so we can use it later
    if inttime.endswith('ms'):
        inttime = float(inttime[:-2])
    else:
        inttime = float(inttime) 
    
    # Read the wavelength and raw count data from the file
    
    with open(filename) as f:
        datafile = csv.reader(f, delimiter=' ')
        for i in range(271): # count from 0 to 271, index of 250.093
            next(datafile)     # and discard the rows
           
        data = {
            'wavelen': [],
            'count': [],
        }
        
        for row in datafile:
            data['wavelen'].append(float(row[0]))
            data['count'].append(float(row[1]))
            
            
    # Get the peak count and the wavelength at which it occurs    
    peakcount = max(data['count'])
    peakidx = data['count'].index(peakcount)
    peakwavelen = data['wavelen'][peakidx]
    
    
    # Interpolate correction factor for each wavelength point
    factor = [interp(specdata['wavelen'], specdata['factor'], wl) for wl in data['wavelen']]
    #print (specdata['wavelen'][0])
    
    # Do the calculations and stuff
    expN = inttime * 100
    expcorrect = expN * 0.184
    irrad = [(data['count'][i] * factor[i]) / expcorrect for i, _ in enumerate(factor)]
    data['irradiance'] = irrad
      
    # Find the peak irradiance
    peakirrad = irrad[peakidx]
    
    nextcol = [irrad[i]*0.000001*10000 for i, _ in enumerate(irrad)]
    data['next']=nextcol
    
    # Find the photon density in 1/m^2/s/nm
    photondens = [irrad[i] / (6.626e-34 * 2.997e8 / data['wavelen'][i] * 1e9) for i, _ in enumerate(irrad)]
    data['photondens'] = photondens

    diff  = data['wavelen'][2]-data['wavelen'][1]
    #print (diff)


    intirrad = 0
    intphotondens = 0
    testList = []
    for i in range(len(irrad) - 1):
        nextavg = (nextcol[i] + nextcol[i+1]) / 2
        wavelenrange = data['wavelen'][i+1] - data['wavelen'][i]
        intirrad = nextavg * wavelenrange
        testList.append(intirrad)
    
    testList.append(0)
        
    #print (testList)
    data['final']=testList
    
 
    # Add each area slice to the integral
    for i in range(len(photondens) - 1):
        irradavg = (irrad[i] + irrad[i+1]) / 2
        wavelenrange = data['wavelen'][i+1] - data['wavelen'][i]
    
    #Interpolate where the count reaches half its maximum on both sides. The data for the right 
    #side is reversed so that wavelength is increasing and interp likes it
    FWHM = interp(data['count'][:peakidx:-1], data['wavelen'][:peakidx:-1], peakcount/2) - \
           interp(data['count'][:peakidx], data['wavelen'][:peakidx], peakcount/2)
    #print (peakwavelen)
    #print (peakcount/2)
    print (FWHM)
    
    rangeVal = float(2.5)
    #print ( FWHM *rangeVal )
    upper = float((FWHM*rangeVal)/2)
   
    
    upperLimit = float(peakwavelen + upper)
    lowerLimit = float(peakwavelen - upper)
    
    #print (upperLimit)
    #print (lowerLimit)
    
    #print (min(enumerate(data['wavelen']), key=lambda x: abs(x[1]-upperLimit)))
    #print (min(enumerate(data['wavelen']), key=lambda x: abs(x[1]-lowerLimit)))
    
    topIndex = min(enumerate(data['wavelen']),key=lambda x: abs(x[1]-upperLimit) )[0]
    bottomIndex = min(enumerate(data['wavelen']),key=lambda x: abs(x[1]-lowerLimit) )[0]
    #print (topIndex)
    #print (bottomIndex)
    
    totalPowerList = []
    for i in range (bottomIndex, topIndex +1):
         #print (testList[i])
         power = testList[i]
         totalPowerList.append(power)
         
    totalPower =sum(totalPowerList)/1E4
 
    # Append the data for the summary so we can write it later
    summarydata.append([ledname, peakwavelen, FWHM, totalPower])
    
    
    # Create our results file
    
    # Ensure our output dir exists
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Creata a CSV file and print wavelength, count, irradiance, and photon density
    with open(os.path.join('output', ledname + '.csv'), 'w') as f:
        outfile = csv.writer(f)
        outfile.writerow(['Wavelength (nm)', 'Raw count', 'Irradiance (W/m^2/nm)', '','W/m^2','Total Power'])
        #outfile.writerow (['','','',[totalPower]])
        for i in range(len(data['wavelen'])):
            outfile.writerow([data['wavelen'][i], data['count'][i], data['irradiance'][i], data['next'][i],  data['final'][i],totalPower])

if not os.path.exists('output'):
    os.makedirs('output')

# Print peak wavelength, FWHM bandwidth, and integrated photon flux and irradiance
with open(os.path.join('output', 'summary.csv'), 'w') as f:
    outfile = csv.writer(f,delimiter=',')
    outfile.writerow(['LED', 'Peak wavelength (nm)', 'FWHM bandwidth (nm)', 'Integrated Irradiance (W/m^2)'])
    for d in summarydata:
        outfile.writerow(d)
        