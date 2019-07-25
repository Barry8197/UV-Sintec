# UV-Sintec

## Sintec - Database 

Contains the files required to build a Database in Postgresql for the Beam Profile of an LED.  Consists of three main python modules called "Table_Create.py" , "Database_Update.py" and "LEDSweep.py".

### Table_Create.py

When executed this module will create a Table called "LED_Data" in the LED database for the postgres user. If the table already exists no new table will be created and the original table will not be affected. 

If you wish to delete the LED_Data table and restart the Database the simplest way is through the Postgresql command line.  

1. Search "SQL Shell (psql)" in the desktop search bar.   

2. Open the SQL Shell command line.  

3. Press Enter 4 times - (PSQL will automatically navigate to the default Server, Database, Port and Postgres User). 

4. Enter the password for the postgres user.  

5. Navigate to the LED database by entering the command -   
` \connect LED ; `  

6. Delete/Drop the table by executing the command -  
` DROP TABLE LED_Data ; `

### Database_Update.py

Contains functions used to both write to and navigate the "LED_Data" Database.  

The functions contained are :  
- write_to_database() - writes the current data to the database in the correct format 
- date_time() - a function used within write_to_database() to timestamp the date entry  
- Table_Search() - a function which returns the relevant entries based on the search conditions of wavelength and product code in database form  
- data_extract() - takes the output from Table_Search() as an input and returns the data in the form of an array based on the column and row you wish to extract
- row_delete() - deletes any unwanted rows

### LEDSweep.py

Executing this module runs the beam profiling protocol.  

This module requests the wavelength, product code , number of sweeps and width of averaging boxcar as inputs. 

An LED is rotated by the specified number of sweeps and its beam profile is found by averaging the profile produced. 

This beam profile is then modelled using both the Cosine and Gaussian Power Models. 

The most most accurate model is chosen and its parameters are stored in a local variable. 

The Root Mean Square Error is outputted and the user is given the choice whether to accept or reject the accuracy of the model. 

If the user chooses to accept, the product code and wavelength are checked against previous entries in the LED_Data database for similar LED's. 

If similar LED's are found the user has the option to update the Beam Profile of the most recent entry or to append this new profile. 

The LED wavelength, product code, model parameters, normalised power profile as well as a time stamp are then stored in the database. 

