# Gives the chronological order of navigating the .ipynb files located in Sintec - Model folder

### Note : ".ipynb" files cannot be opened on Github and must be downloaded and opened with Jupyter

Each .ipynb file contains a description of its contents as well as a description of the functions in the file. 

## Navigating the ipynb files in chronological order

1. Single_LED_Hemisphere_Model.ipynb 
   * This notebook introduces the idea of modelling the beam profile of an LED as a hemisphere. It models the LED Beam Profile as a normalized power source that falls off with 1 over distance squared. The notebook contains polar , 2D and 3D plots. The notebook also looks at how the shape of the beam profile changes with increasing distance. 

2. Double_LED_Hemisphere_Model.ipynb
   * This notebook builds upon the Single Hemisphere Model. This notebook looks at the combined beam profile of two LED's modelled as a hemishpere whose power drops off with 1 over distance squared. The notebook consists of two interactive plots with sliders which change the intensisty and origin of two sources. These can be altered to give a flat combined LED response. The final plot is a polar plot which shows the flat response in a polar plane

3. I.Moreno_LED_Model.ipynb
   * [Modelling the Radiation Pattern of LED's](https://www.osapublishing.org/DirectPDFAccess/9CC83EE3-F677-E72D-2F8A1F584096DB23_149957/oe-16-3-1808.pdf?da=1&id=149957&seq=0&mobile=no) by Ivan Moreno and Ching-Cherng Sun is a paper which provides equations that can be used to accurately model the Beam Profile of LED's. This notebook looks to replicate some examples of Beam Profiles contained in the paper
  
4. Cosine_Power_Model.ipynb
   * This notebook contains all the functions required to fit the Cosine modelling equation presented in the above paper to any LED beam profile. This notebook is the foundation for the python module "Cosine_Power_Model.py" with an example of how to use the functions included at the end. 

5. Gaussian_Power_Model.ipynb
   * Identitical to "Cosine_Power_Model.ipynb" except it uses an exponential equation to model the beam profile of an LED. 

6. Cosine_XY_Power_Model.ipynb
   * As some LED beam profiles are non uniform, the paper by Ivan Moreno accounts for this by introducing a model which accounts for a different beam profile in the XX axis and YY axis.

7. Gaussian_XY_Power_Model.ipynb
   * Same as "Cosine_XY_Power_Model.ipynb".

8. Gaussian_vs._Cosine.ipynb
   * This notebook uses the Nichia Corp LED to highlight how both the "Cosine_Power_Model.py" and "Gaussian_Power_Model.py" can be used to model the same beam profile and how while both are powerful modelling equations, there are differences in accuracy. 

9. Nichia_2D_Array.ipynb
   * This notebook firsts models the Nichia Corp LED using the Cosine_Power_Model. The aim of this notebook is to produce a maximally flat response when several LED's are arranged in a 2D array. The degree of freedom for the optimisation is the location of the LED's relative to a common x axis. A description of each function is included in the notebook with the final script performing the optimisation for an increasing number of LED's. The optimum location of the LED is printed at each iteration along with beam profile of the added LED's and the combined Beam Profile. The section over which the combined Beam Profile is optomised is also highlighted. 
