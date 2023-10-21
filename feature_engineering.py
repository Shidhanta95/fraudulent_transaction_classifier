import numpy as np
import pandas as pd
from datavisualization import  visualise_data

#Average time delta between transactions used in calculations
def list_diff(x_input):
    if len(x_input)<2:
        xdiff = 0
        delta_mean=0
    else:
        xdiff = [x_input[n]-x_input[n-1] for n in range(1,len(x_input))]
        delta_mean = np.mean(xdiff)
    return delta_mean

#Delta before last transaction used in calculations
def delta_last(x_input):
    if len(x_input)<2:
        delta_l=0
    else:
        delta_l = x_input[-1]-x_input[-2]
    return delta_l


def feature_engineer():
    data = visualise_data()
#type Orig ==first letter from nameOrig 
    data['New_TypeOrig']= data['nameOrig'].apply(lambda x: x[0])
    
    #type Dest ==first letter from nameDest
    data['New_TypeDest']= data['nameDest'].apply(lambda x: x[0])


    #Average time delta between transactions Orig used in calculations
    x_input = data.groupby('nameOrig')['step'].apply(list).reset_index(name='info')
    data = pd.merge(data, x_input, how='left', on='nameOrig')
    data['New_Delta_Time_Tr_Orig'] = data['info'].apply(lambda x: list_diff(x))
    
    #time to previous transaction Orig used in calculations
    data['New_Delta_Last_Tr_Orig']= data['info'].apply(lambda x: delta_last(x))

    #Average time delta between transactions Dest !not used in calculations
    x_input_dest = data.groupby('nameDest')['step'].apply(list).reset_index(name='info_2')
    data = pd.merge(data, x_input_dest, how='left', on='nameDest')
    data['New_Delta_Time_Tr_Dest'] = data['info_2'].apply(lambda x: list_diff(x) )

    #time to previous transaction Dest !not used in calculations
    data['New_Delta_Last_Tr_Dest']= data['info_2'].apply(lambda x: delta_last(x))

    #Removing extra columns
    data = data.drop(columns=['info','info_2'])
    
    #delete first letter Orig , Dest
    data['nameOrig']=data['nameOrig'].apply(lambda x: x[1:])
    data['nameDest']=data['nameDest'].apply(lambda x: x[1:])
    
    #used in calculations
    data['res_data']=pd.to_datetime(data['step'], unit='h', origin=pd.Timestamp('2000-01-01'))


    # Select the date, days of the week, hours, month  !not used in calculations
    data['date'] = data.res_data.dt.date
    data['day_of_week'] = data.res_data.dt.dayofweek
    data['hour'] = data.res_data.dt.hour
    data['month'] = data.res_data.dt.month
    data.to_csv('financial_transaction_cleansed_data.csv', index=False)

    return data


feature_engineer()

