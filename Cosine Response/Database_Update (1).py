import pandas as pd
import time
from sqlalchemy import create_engine

def write_to_database(product_code , wavelength , model , Param , RMSE , Power , df ) :
    #engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/LED")
    Date , Time = date_time()

    param1 = [item[0] for item in Param]
    param2 = [item[1] for item in Param]
    param3 = [item[2] for item in Param]
    try :
        param4 = [item[3] for item in Param]
        table = [(Date) , (Time) , (product_code) , (wavelength) , (model) , (RMSE) , (param1) , (param2) , (param3) , (param4) , (Power)]
    except :
        table = [(Date) , (Time) , (product_code) , (wavelength) , (model) , (RMSE) , (param1) , (param2) , (param3) , ("n/a") , (Power)]

    df1 = pd.DataFrame([table], columns=["Date" , "Time" , "Product Code" , "Wavelength" , "Model"  , "RMSE"
                                         , "Param1" , "Param2" , "Param3" , "Param4" , "Normalized Power"])


    #df1.to_sql('' , con = engine , if_exists = "append" , index = False)
    #df = pd.read_sql_query('select * from "table_name"' , con = engine)
    df = df.append(df1 , ignore_index = True)

    count = 0
    index = []
    for item in df.duplicated(["Product Code" , "Wavelength" , "Model"]) :
        if item == True :
            count += 1
            if [df.loc[count][2],df.loc[count][3] , df.loc[count][4]] == [product_code , wavelength , model] :
                index.append(count)
                
    print(index)

    if len(index) > 0:
        check = False
        print("This LED has been identified as a duplicate")
        print("")
        while check == False :
            update = input("Do you want to update the LED Model in the Database (y/n) :")
            if update.lower().strip() == "y" :
                if len(index) > 1 :
                    df = df.drop(index[-2]).reset_index(drop = True)
                else :
                    df = df.drop(index[-1]-1).reset_index(drop = True)
                check = True
            elif update.lower().strip() == "n" :
                check = True
            else :
                print("")
                print("Error please select y/n")
                check = False
            


    #df.to_sql('' , con = engine , if_exists = "replace" , index = False)
    
    return df


def date_time():
    datetime_object = datetime.datetime.now()
    time = str(datetime_object.time())[:8]
    date = str(datetime_object.date())
    
    return date , time

def Table_Search():
    wavelength = str(input("Enter Manufacturer Wavelength in nm :")).replace(" ", "")
    product_code = str(input("Enter Product Code in form xxxx-xxxx :")).replace(" ", "")
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/LED")
    
    df = pd.read_sql_query('select * from "table_name"' , con = engine)
    df1 = df.loc[(df["Wavelength"] == wavelength) & (df["Product Code"] == product_code)] 
    
    return df1