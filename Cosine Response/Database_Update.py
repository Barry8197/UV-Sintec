import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
import ipywidgets as widgets
from ipywidgets import interactive
from IPython.display import display
import warnings


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
        print("This photodiode has been identified as a duplicate")
        print("")
        while check == False :
            update = input("Do you want to update the Photodiode Model in the Database (y/n) :")
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


def Database_Search() :
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")
    
    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)
    
    items = ['All']+sorted(df['product_code'].unique().tolist())

    def view(x=''):
        x = x.replace(" " , "")
        filtered = df["product_code"].str.contains(x)

        if x =='': 
            return display(df)

        elif len(df[filtered]) > 0 : 
            return display(df[filtered])

        else :
            return print("This product code does not match any Photodiodes's in the Database")

    product_code = widgets.Text(
        value='',
        placeholder='Enter Product Code',
        description='Input:',
        disabled=False
    )
    
    return interactive(view, x=product_code)

def Data_Extract() :
    product_code = str(input("Enter Full Product Code :")).replace(" ", "")

    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")

    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)
    df1 = df.loc[(df["product_code"] == product_code)] 

    if len(df1) > 0 :
        display(df1)
        row = int(input("Which Row do you wish to extract data from :"))

        try :
            warnings.filterwarnings("ignore")
            df1[item][row] = pd.to_numeric(df1[item][row][1:-1].split(","))        
        except :
            pass

        items_list = [df1.columns.values.tolist()] + df1.values.tolist()
        print("The Data has been saved to variable 'items_list'")
        print("The location of the data corresponds to the loaciton of the column heading ")
        print("e.g. wavelength heading is item_list[0][3] and the wavelength value is item_list[1][3]")

        for i in range(len(items_list[0])) :
            print("%i. %s" %(i , items_list[0][i]))

        return items_list

    else :
        return print("This product code does not match any photodiode's in the Database")
    
def Row_Delete() :
    product_code = str(input("Enter Full Product Code :")).replace(" ", "")
    
    engine = create_engine("postgresql://postgres:uv-sintec@localhost:5432/Photodiode")
    
    df = pd.read_sql_query('select * from "photodiode_data"' , con = engine)
    df1 = df.loc[(df["product_code"] == product_code)]
    
    if len(df1) > 0 :
        
        display(df1)
        index = int(input("Select the row you wish to delete :"))

        if index in df1.index.values :
            df = df.drop(index).reset_index(drop = True)

            df.to_sql('photodiode_data' , con = engine , if_exists = "replace" , index = False)
        else :
            return print("The row you selected does not correspond to the product code entered")
    else :
        return print("This product code does not match any photodiode's in the Database")        