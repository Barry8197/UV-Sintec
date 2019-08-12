import psycopg2

try : 
    conn = psycopg2.connect(database = "LED_Measurements" , user = "postgres" , password = "uv-sintec" , host = "localhost" , port = "5432")
    
except :
    print("Unable to connect to Database")
    
cur = conn.cursor()

try :
    cur.execute("CREATE TABLE led_measurements (date varchar , time varchar , product_code varchar , label_wavelength varchar , current varchar , exposure_time varchar , boxcar varchar , scans varchar , background varchar , device_number varchar , peak_wavelength varchar , fwhm varchar , integrated_irradiance varchar);")
    
except :
    print("Unable to create table")
    
conn.commit()
conn.close()
cur.close()
