# LED Measurements

## Table_Create.py

Executed by running 

When executed this module will create a Table called "LED_Data" in the LED database for the postgres user. If the table already exists no new table will be created and the original table will not be affected.

If you wish to delete the LED_Data table and restart the Database the simplest way is through the Postgresql command line.

Search "SQL Shell (psql)" in the desktop search bar.

Open the SQL Shell command line.

Press Enter 4 times - (PSQL will automatically navigate to the default Server, Database, Port and Postgres User).

Enter the password for the postgres user.

Navigate to the LED database by entering the command -
\connect LED ;

Delete/Drop the table by executing the command -
DROP TABLE LED_Data ;
