# UV-Sintec

## Sintec - Database 

Contains the files required to build a Database in Postgresql for the Beam Profile of an LED.  Consists of three main python modules called "Table_Create.py" , "Database_Update.py" and "LEDSweep.py". These files are discussed to a greater extent in the README.md file in Sintec - Database.

This folder also contains the python modules "Cosine_Power_Model.py" and "Gaussian_Power_Model.py". These files are imported into the "LEDSweep.py" and are included this folder to simplify the importing of the modules. They are discussed to a greater extent in the Sintec - Model folder.

## Sintec - Model

Contains 2 ".csv" files which are two data files containing beam profiles found online.

"Nichia.csv" is the beam profile for the [NSPW345CS LED](https://www.alldatasheet.com/datasheet-pdf/pdf/240328/NICHIA/NSPW345CS.html?) from Nichia Corp.

"CREE_LED4" is the beam profile for the [XLamp XR-E LED](https://www.cree.com/led-components/media/documents/XLamp7090XRE-16F.pdf) from Cree Corp. 

Contains 2 ".py" files called "Cosine_Power_Model.py" and "Gaussian_Power_Model.py". These files are converted python modules from the jupyter notebook files "Cosine_Power_Model.ipynb" and Gaussian_Power_Model.ipynb" respectively. 

All other files are Jupyter Notebooks of the form ".ipynb". These files cannot be viewed on Github and must be downloaded and opened using Jupyter Notebook. These files are discussed to a greter extent in the README.md file in Sintec - Model

## LED Measurements

Contains 9 ".txt", 8 of which contain measurements from a spectrometer for a examplar LED with the final file containing the final specifications for the LED

Contains 3 ".py" files whose function is explained in the folder

Contains 1 ".ipynb" file which is given as an examplar of the operation of the ".py" files

The Output folder is of importance as it contains 8 csv files containing results of calculations completed as part of the Automate_Working_Final.py file as well as a csv file containing a summary of the calculations. 

## Spectral Line Shaping

Contains a ".py" file whose funcitons are explained in the folder

Contains a ".ipynb" file which models a weighted combination of a Lorentz and Gaussian functions to each ".txt" LED measurement file contained in the folder.

## Genetic Algorithm Models

Models the Beam profiles of LED's using a Genetic Algorthim as opposed to a regression model in Sintec - Model

Contains 2 ".csv" files which are two data files containing beam profiles found online.

"Nichia.csv" is the beam profile for the [NSPW345CS LED](https://www.alldatasheet.com/datasheet-pdf/pdf/240328/NICHIA/NSPW345CS.html?) from Nichia Corp.

"CREE_LED4" is the beam profile for the [XLamp XR-E LED](https://www.cree.com/led-components/media/documents/XLamp7090XRE-16F.pdf) from Cree Corp. 

Contains 2 ".py" files called "CPM_Genetic_Algorithm.py" and "Gauss_Genetic_Algorithm.py". These files are converted python modules from the jupyter notebook files "CPM_Genetic_Algorithm.ipynb" and Gauss_Genetic_Algorithm.ipynb" respectively. The two .ipynb files contain comment explanations of the code

All other files are Jupyter Notebooks of the form ".ipynb". These files cannot be viewed on Github and must be downloaded and opened using Jupyter Notebook. These files are discussed to a greter extent in the README.md file in Sintec - Model

## Beam_Profile_Genetic_Algorithm_Optimization

Uses the above Genetic Algorithm Models to model the beam profile of the Nichia Corp LED Beam Profile.

It then uses another Genetic Algorithm to optomize the addition of multiple Beam Profiles in the aim of optomizing the summation to have a flat response. 

The algorithm uses a cartesian coordinate plane to place the LED Beam Profile Origin with a flat response achieved with the optimal solution having the LED's correctly spaced in the x-y plane at a certain distance away.

## Beam Profile & Cosine Response

Contains files need to extract the beam profile of an LED. such files include the Arduino code and python scripts used in orer to operate the apparatus correctly. The code should offer to write the results to the database and show the 3D model of the beam Profile

The steps needed to get the beam profile are summarised in Instructions (Beam Profile) along with examples of how the beam profile should look.

## Genetic Algorithm Spectral Model

Contains 12 ".txt" files which correspond to the spectral content of 12 distinct LEDs

Contains one ".csv" file which contains the spectral content of sunlight downloaded [online](https://www.pveducation.org/pvcdrom/appendices/standard-solar-spectra)

Contains one ".jpeg" file which explains the method of crossover used for the genetic alogorithm

Contains a ".py" file taken from Spectral Line Shaping folder and is a module which is used to model the spectral shape of LEDs

Contains a ".ipynb" file which contains the Genetic Algorithm used to fit the weighted sum of LEDs to the solar spectrum

