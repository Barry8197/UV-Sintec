# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:14:11 2019

@author: Morrison-Lab
"""

import psycopg2

try : 
    conn = psycopg2.connect(database = "LED" , user = "postgres" , password = "uv-sintec" , host = "localhost" , port = "5432")
    
except :
    print("Unable to connect to Database")
    
cur = conn.cursor()

try :
    cur.execute("CREATE TABLE LED_Data (Date varchar , Time varchar , Product_Code varchar , Wavelength varchar , Model varchar , Input_Angle_1 float, RMSE_Angle_1 float ,Param1_Angle_1 float[] , Param2_Angle_1 float[] , Param3_Angle_1 float[] , Param4_Angle_1 float[] , Normalized_Power_Angle_1 float[], Input_Angle_2 float, RMSE_Angle_2 float ,Param1_Angle_2 float[] , Param2_Angle_2 float[] , Param3_Angle_2 float[] , Param4_Angle_2 float[] , Normalized_Power_Angle_2 float[], Input_Angle_3 float, RMSE_Angle_3 float ,Param1_Angle_3 float[] , Param2_Angle_3 float[] , Param3_Angle_3 float[] , Param4_Angle_3 float[] , Normalized_Power_Angle_3 float[], Input_Angle_4 float, RMSE_Angle_4 float ,Param1_Angle_4 float[] , Param2_Angle_4 float[] , Param3_Angle_4 float[] , Param4_Angle_4 float[] , Normalized_Power_Angle_4 float[]);")
except :
    print("Unable to create table")
    
conn.commit()
conn.close()
cur.close()