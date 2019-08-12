# LED Measurements

## Table_Create.py

Executed by running -
` %run Table_Create.py `

When executed this module will create a Table called "led_measurements" in the LED_Measurements database for the postgres user. If the table already exists no new table will be created and the original table will not be affected.

If you wish to delete the led_measurements table and restart the Database the simplest way is through the Postgresql command line.

Search "SQL Shell (psql)" in the desktop search bar.

Open the SQL Shell command line.

Press Enter 4 times - (PSQL will automatically navigate to the default Server, Database, Port and Postgres User).

Enter the password for the postgres user.

Navigate to the LED database by entering the command -
` \connect LED_Measurements ; `

Delete/Drop the table by executing the command -
` DROP TABLE led_measurements ; `

## Database_Update.py

Contains functions used to both write to and navigate the "led_measurements" Database.  

The functions contained are :  
- write_to_database() - takes the summary data and product code as inputs and writes the summary data to the database in the correct format 
- date_time() - a function used within write_to_database() to timestamp the date entry  
- Database_Search() - a interactive function which searches the database based on an entire or incompltete product code, wavelength and device number and returns all matched found in the database
- Data_Extract() - returns an array consisting of a specific row when a product code has been searched 
- Row_Delete() - deletes any unwanted rows

## Automate_Working_Final.py 

Emily 

