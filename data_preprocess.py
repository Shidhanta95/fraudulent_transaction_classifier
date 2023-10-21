from data_analysis import analyse_data
import numpy as np
import pandas as pd

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



def data_preprocessing(data):
    
 #number of transactions Orig !not used in calculations
    dict_count_sent = data['nameOrig'].value_counts()
    data['New_TotalOrig']= data['nameOrig'].map(dict_count_sent) 
    
    #number of transactions Dest !not used in calculations
    dict_count_get = data['nameDest'].value_counts()
    data['New_TotalDest']= data['nameDest'].map(dict_count_get)
    
    #average transaction Orig !not used in calculations
    trans_mean_orig = data.groupby("nameOrig")["amount"].aggregate(['mean'])
    dict_trans_mean_orig=trans_mean_orig.to_dict()
    value_dict_trans_mean_orig=dict_trans_mean_orig['mean']
    data['New_TotalMeanOrig']=data['nameOrig'].map(value_dict_trans_mean_orig)
    
    #average transaction Dest !not used in calculations
    trans_mean_dest = data.groupby("nameDest")["amount"].aggregate(['mean'])
    dict_trans_mean_dest=trans_mean_dest.to_dict()
    value_dict_trans_mean_dest=dict_trans_mean_dest['mean']
    data['New_TotalMeanDest']=data['nameDest'].map(value_dict_trans_mean_dest)
    
    #Amount of transactions with participation Orig !not used in calculations
    trans_sum_orig = data.groupby("nameOrig")["amount"].aggregate([sum])
    dict_trans_sum_orig=trans_sum_orig.to_dict()
    value_dict_trans_sum_orig=dict_trans_sum_orig['sum']
    data['New_TotalSumOrig']=data['nameOrig'].map(value_dict_trans_sum_orig)
    
    #Amount of transactions with participation Dest !not used in calculations
    trans_sum_dest = data.groupby("nameDest")["amount"].aggregate([sum])
    dict_trans_sum_dest=trans_sum_dest.to_dict()
    value_dict_trans_sum_dest=dict_trans_sum_dest['sum']
    data['New_TotalSumDest']=data['nameDest'].map(value_dict_trans_sum_dest)
    
    #type Orig ==first letter from nameOrig 
    data['New_TypeOrig']= data['nameOrig'].apply(lambda x: x[0])
    
    #type Dest ==first letter from nameDest
    data['New_TypeDest']= data['nameDest'].apply(lambda x: x[0])
    
    #Average time delta between transactions Orig !not used in calculations
    x_input = data.groupby('nameOrig')['step'].apply(list).reset_index(name='info')
    data = pd.merge(data, x_input, how='left', on='nameOrig')
    data['New_Delta_Time_Tr_Orig'] = data['info'].apply(lambda x: list_diff(x))
    #time to previous transaction Orig !not used in calculations
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
    
    #!not used in calculations
    data['res_data']=pd.to_datetime(data['step'], unit='h', origin=pd.Timestamp('2000-01-01'))
    
    ### Select the date, days of the week, hours, month  !not used in calculations
    data['date'] = data.res_data.dt.date
    data['day_of_week'] = data.res_data.dt.dayofweek
    data['hour'] = data.res_data.dt.hour
    data['month'] = data.res_data.dt.month

    data.drop(columns = ['step', 'nameOrig','nameDest', 'isFlaggedFraud', 
                          'New_TotalOrig', 'New_TotalDest', 'New_TotalMeanOrig',
                          'New_TotalMeanDest', 'New_TotalSumOrig', 'New_TotalSumDest', 
                          'New_Delta_Time_Tr_Orig','New_Delta_Last_Tr_Orig', 
                          'New_Delta_Time_Tr_Dest','New_Delta_Last_Tr_Dest', 
                          'res_data', 'date', 'day_of_week', 'hour','month'], 
               inplace=True)


    #due to the fact that we have few unique values, we will go by the simple way of converting categorical features
    data_test = pd.get_dummies(data, prefix = ['type', 'New_TypeOrig', 'New_TypeDest'], drop_first = True)
    return data_test

def data_preprocess():
    data, num_features, cat_features  = analyse_data()
    # Transactions which are detected as fraud are cancelled, 
    # so for fraud detection these columns 
    # (oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest ) must not be used.

    # nameOrig - customer who started the transaction
    # oldbalanceOrg - initial balance before the transaction
    # newbalanceOrig - new balance after the transaction.
    # nameDest - customer who is the recipient of the transaction
    
    # oldbalanceDest - initial balance recipient before the transaction.
        # Note that there is not information for customers that start with M (Merchants).

    # newbalanceDest - new balance recipient after the transaction. 
        # Note that there is not information for customers that start with M (Merchants). 
    
    # isFraud - This is the transactions made by the fraudulent agents inside the simulation. 
        # In this specific dataset the fraudulent behavior of the agents aims to profit by taking control or customers accounts and try to empty the funds by transferring to another account and then cashing out of the system.

    # isFlaggedFraud - The business model aims to control massive transfers from one account to another and flags illegal attempts. 
        # An illegal attempt in this dataset is an attempt to transfer more than 200.000 in a single transaction.


    
    data = data_preprocessing(data)
    print(data.head())
    categorical_features = data.select_dtypes("object").columns
    numerical_features = data.select_dtypes("number").columns
    return data, numerical_features, categorical_features

