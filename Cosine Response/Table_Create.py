import psycopg2

try : 
    conn = psycopg2.connect(database = "LED" , user = "postgres" , password = "uv-sintec" , host = "localhost" , port = "5432")
    
except :
    print("Unable to connect to Database")
    
cur = conn.cursor()

try :
    cur.execute("CREATE TABLE led_data (date varchar , time varchar , product_code varchar , wavelength varchar , model varchar , input_angle_1 float,  rmse_angle_1 float ,param1_angle_1 float[] , param2_angle_1 float[] , param3_angle_1 float[] , param4_angle_1 float[] , normalized_power_angle_1 float[] , input_angle_2 float,  rmse_angle_2 float ,param1_angle_2 float[] , param2_angle_2 float[] , param3_angle_2 float[] , param4_angle_2 float[] , normalized_power_angle_2 float[] , input_angle_3 float,  rmse_angle_3 float ,param1_angle_3 float[] , param2_angle_3 float[] , param3_angle_3 float[] , param4_angle_3 float[] , normalized_power_angle_3 float[] , input_angle_4 float,  rmse_angle_4 float ,param1_angle_4 float[] , param2_angle_4 float[] , param3_angle_4 float[] , param4_angle_4 float[] , normalized_power_angle_4 float[] , model_angle_1 , model_angle_2 , model_angle_3 , model_angle_4);")
    
except :
    print("Unable to create table")
    
conn.commit()
conn.close()
cur.close()
