import numpy as np
import pandas as pd
from datavisualization import  visualise_data
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler

def SMOTEUpsampling(data):
    #smote based upsampling 
    # transform the dataset
    oversample = RandomOverSampler(sampling_strategy='minority')
    
    x = data.drop(columns=['isFraud'])
    y = data['isFraud']
    # x = np.nan_to_num(x)
    # y = np.nan_to_num(y)
    x,y = oversample.fit_resample(x,y)
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)

    df_concat = pd.concat([x,y], axis=1) 
    return df_concat



def feature_engineer():
    data = visualise_data()
    #Class balancing 
    data_mod = SMOTEUpsampling(data)

    data_mod.to_csv('financial_transaction_cleansed_data.csv', index=False)

    return data_mod


feature_engineer()

