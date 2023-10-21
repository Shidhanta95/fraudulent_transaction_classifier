from data_analysis import analyse_data
import numpy as np
import pandas as pd



def data_preprocessing(data):
    

     #number of transactions Orig used in calculations
    dict_count_sent = data['nameOrig'].value_counts()
    data['New_TotalOrig']= data['nameOrig'].map(dict_count_sent) 
    
    #number of transactions Dest used in calculations
    dict_count_get = data['nameDest'].value_counts()
    data['New_TotalDest']= data['nameDest'].map(dict_count_get)
    
    #average transaction Orig used in calculations
    trans_mean_orig = data.groupby("nameOrig")["amount"].aggregate(['mean'])
    dict_trans_mean_orig=trans_mean_orig.to_dict()
    value_dict_trans_mean_orig=dict_trans_mean_orig['mean']
    data['New_TotalMeanOrig']=data['nameOrig'].map(value_dict_trans_mean_orig)

    #average transaction Dest used in calculations
    trans_mean_dest = data.groupby("nameDest")["amount"].aggregate(['mean'])
    dict_trans_mean_dest=trans_mean_dest.to_dict()
    value_dict_trans_mean_dest=dict_trans_mean_dest['mean']
    data['New_TotalMeanDest']=data['nameDest'].map(value_dict_trans_mean_dest)
    
    #Amount of transactions with participation Orig used in calculations
    trans_sum_orig = data.groupby("nameOrig")["amount"].aggregate([sum])
    dict_trans_sum_orig=trans_sum_orig.to_dict()
    value_dict_trans_sum_orig=dict_trans_sum_orig['sum']
    data['New_TotalSumOrig']=data['nameOrig'].map(value_dict_trans_sum_orig)


    #average transaction Dest used in calculations
    trans_mean_dest = data.groupby("nameDest")["amount"].aggregate(['mean'])
    dict_trans_mean_dest=trans_mean_dest.to_dict()
    value_dict_trans_mean_dest=dict_trans_mean_dest['mean']
    data['New_TotalMeanDest']=data['nameDest'].map(value_dict_trans_mean_dest)

    #Amount of transactions with participation Orig used in calculations
    trans_sum_orig = data.groupby("nameOrig")["amount"].aggregate([sum])
    dict_trans_sum_orig=trans_sum_orig.to_dict()
    value_dict_trans_sum_orig=dict_trans_sum_orig['sum']
    data['New_TotalSumOrig']=data['nameOrig'].map(value_dict_trans_sum_orig)    

   #Amount of transactions with participation Dest used in calculations
    trans_sum_dest = data.groupby("nameDest")["amount"].aggregate([sum])
    dict_trans_sum_dest=trans_sum_dest.to_dict()
    value_dict_trans_sum_dest=dict_trans_sum_dest['sum']
    data['New_TotalSumDest']=data['nameDest'].map(value_dict_trans_sum_dest)

    
    return data

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

data_preprocess()