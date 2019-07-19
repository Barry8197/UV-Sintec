import pandas as pd
import datetime
import time
from sqlalchemy import create_engine


def write_to_database_diode(product_code 
                      , input_angle_1 , Params1 , RMSE1 , Power1
                      , input_angle_2 , Params2 , RMSE2 , Power2
                      , input_angle_3 , Params3 , RMSE3 , Power3
                      , input_angle_4 , Params4 , RMSE4 , Power4
                      , model1, model2, model3, model4
                      ) :
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")
    Date , Time = date_time()

    param1_1 = [item[0] for item in Params1]
    param2_1 = [item[1] for item in Params1]
    param3_1 = [item[2] for item in Params1]
    
    param1_2 = [item[0] for item in Params2]
    param2_2 = [item[1] for item in Params2]
    param3_2 = [item[2] for item in Params2]
    
    param1_3 = [item[0] for item in Params3]
    param2_3 = [item[1] for item in Params3]
    param3_3 = [item[2] for item in Params3]
    
    param1_4 = [item[0] for item in Params4]
    param2_4 = [item[1] for item in Params4]
    param3_4 = [item[2] for item in Params4]
    
    try :
        param4_1 = [item[3] for item in Params1]
        param4_2 = [item[3] for item in Params2]
        param4_3 = [item[3] for item in Params3]
        param4_4 = [item[3] for item in Params4]
        table = [(Date) , (Time) , (product_code) 
        , (input_angle_1) , (RMSE1) , (param1_1) , (param2_1) , (param3_1) , (param4_1) , (Power1)
        , (input_angle_2) , (RMSE2) , (param1_2) , (param2_2) , (param3_2) , (param4_2) , (Power2)
        , (input_angle_3) , (RMSE3) , (param1_3) , (param2_3) , (param3_3) , (param4_3) , (Power3)
        , (input_angle_4) , (RMSE4) , (param1_4) , (param2_4) , (param3_4) , (param4_4) , (Power4)
        , (model1) , (model2) , (model3) , (model4)
        ]
    except :
        #table = [(Date) , (Time) , (product_code) , (wavelength) , (model) , (RMSE) , (param1) , (param2) , (param3) , ([]) , (Power)]
        table = [(Date) , (Time) , (product_code)  
        , (input_angle_1) , (RMSE1) , (param1_1) , (param2_1) , (param3_1) , ([]) , (Power1)
        , (input_angle_2) , (RMSE2) , (param1_2) , (param2_2) , (param3_2) , ([]) , (Power2)
        , (input_angle_3) , (RMSE3) , (param1_3) , (param2_3) , (param3_3) , ([]) , (Power3)
        , (input_angle_4) , (RMSE4) , (param1_4) , (param2_4) , (param3_4) , ([]) , (Power4)
        , (model1) , (model2) , (model3) , (model4)
        ]
    df1 = pd.DataFrame([table], columns=["date" , "time" , "product_code" 
                                         ,"input_angle_1" ,"rmse_angle_1", "param1_angle_1" , "param2_angle_1" , "param3_angle_1" , "param4_angle_1" , "normalized_power_angle_1"
                                         ,"input_angle_2" ,"rmse_angle_2", "param1_angle_2" , "param2_angle_2" , "param3_angle_2" , "param4_angle_2" , "normalized_power_angle_2"
                                         ,"input_angle_3" ,"rmse_angle_3", "param1_angle_3" , "param2_angle_3" , "param3_angle_3" , "param4_angle_3" , "normalized_power_angle_3"
                                         ,"input_angle_4" ,"rmse_angle_4", "param1_angle_4" , "param2_angle_4" , "param3_angle_4" , "param4_angle_4" , "normalized_power_angle_4"
                                         , "model_angle_1" , "model_angle_2" , "model_angle_3" , "model_angle_4" ])


    df1.to_sql('photodiode_data' , con = engine , if_exists = "append" , index = False)
    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)

    index = []
    count = 0
    for item in df.duplicated(["product_code"]):
        if [df.loc[count][2],df.loc[count][3] ] == [product_code] :
                index.append(count)
        count += 1

    if len(index) > 1:
        check = False
        print("This LED has been identified as a duplicate")
        print("")
        while check == False :
            update = input("Do you want to update the LED Model in the Database (y/n) :")
            if update.lower().strip() == "y" :
                if len(index) > 1 :
                    df = df.drop(index[-2]).reset_index(drop = True)
                check = True
            elif update.lower().strip() == "n" :
                check = True
            else :
                print("")
                print("Error please select y/n")
                check = False


    df.to_sql('photodiode_data' , con = engine , if_exists = "replace" , index = False)
    
    return df



def date_time():
    datetime_object = datetime.datetime.now()
    time = str(datetime_object.time())[:8]
    date = str(datetime_object.date())
    
    return date , time


def Table_Search():
    wavelength = str(input("Enter Manufacturer Wavelength in nm :")).replace(" ", "")+"nm"
    product_code = str(input("Enter Full Product Code :")).replace(" ", "")
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")
    
    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)
    df1 = df.loc[(df["product_code"] == product_code)] 
    
    return df1

def data_extract(df) :
    row = int(input("Which Row do you wish to extract data from :"))
    column = str(input("Which Column do you wish to extract data from :")).replace(" " , "")
    data = []
    try :
        for item in df[column][row][1:-1].split(','):
            data.append(float(item))
    except :
        print("This Column does not exist")
        
    return data

def row_delete() :
    df = Table_Search()
    
    display(df)
    
    index = int(input("Select Column You Wish to delete :"))
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")
    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)
    
    df = df.drop(index).reset_index(drop = True)
    
    df.to_sql('photodiode_data' , con = engine , if_exists = "replace" , index = False)