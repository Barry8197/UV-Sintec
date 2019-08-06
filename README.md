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

