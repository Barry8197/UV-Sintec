import pandas as pd
import datetime
import time
from sqlalchemy import create_engine


def write_to_database(product_code , wavelength , model , Param , RMSE , Power) :
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/LED")
    Date , Time = date_time()

    param1 = [item[0] for item in Param]
    param2 = [item[1] for item in Param]
    param3 = [item[2] for item in Param]
    try :
        param4 = [item[3] for item in Param]
        table = [(Date) , (Time) , (product_code) , (wavelength) , (model) , (RMSE) , (param1) , (param2) , (param3) , (param4) , (Power)]
    except :
        table = [(Date) , (Time) , (product_code) , (wavelength) , (model) , (RMSE) , (param1) , (param2) , (param3) , ([]) , (Power)]

    df1 = pd.DataFrame([table], columns=["date" , "time" , "product_code" , "wavelength" , "model"  , "rmse"
                                         , "param1" , "param2" , "param3" , "param4" , "normalized_power"])


    df1.to_sql('test_led' , con = engine , if_exists = "append" , index = False)
    df = pd.read_sql_query('select * from "test_led"' , con = engine)

    index = []
    count = 0
    for item in df.duplicated(["product_code" , "wavelength"]):
        if [df.loc[count][2],df.loc[count][3] ] == [product_code , wavelength] :
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


    df.to_sql('test_led' , con = engine , if_exists = "replace" , index = False)
    
    return df



def date_time():
    datetime_object = datetime.datetime.now()
    time = str(datetime_object.time())[:8]
    date = str(datetime_object.date())
    
    return date , time


def Table_Search():
    wavelength = str(input("Enter Manufacturer Wavelength in nm :")).replace(" ", "")+"nm"
    product_code = str(input("Enter Full Product Code :")).replace(" ", "")
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/LED")
    
    df = pd.read_sql_query('select * from "test_led"' , con = engine)
    df1 = df.loc[(df["wavelength"] == wavelength) & (df["product_code"] == product_code)] 
    
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
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/LED")
    df = pd.read_sql_query('select * from "test_led"' , con = engine)
    
    df = df.drop(index).reset_index(drop = True)
    
    df.to_sql('test_led' , con = engine , if_exists = "replace" , index = False)