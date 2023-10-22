import pandas as pd

def load_data():
    data = pd.read_csv('data.csv')
    #data = data_raw.iloc[:100,:]
    print(data.head())
    return data

load_data()
