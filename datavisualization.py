import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker 
from data_preprocess import analyse_data


def visualise_data():
    #heatmap
    # data, numerical_features, categorical_features = feature_engineer()
    data, numerical_features, categorical_features  = analyse_data()
    # data_n = data[['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest',
    #    'newbalanceDest', 'isFraud', 'isFlaggedFraud', 'New_TotalOrig',
    #    'New_TotalDest', 'New_TotalMeanOrig', 'New_TotalMeanDest',
    #    'New_TotalSumOrig', 'New_TotalSumDest', 'New_Delta_Time_Tr_Orig',
    #    'New_Delta_Last_Tr_Orig', 'New_Delta_Time_Tr_Dest',
    #    'New_Delta_Last_Tr_Dest', 'day_of_week', 'hour', 'month']]
    # # plt.figure(figsize=(6,4))
    # mask = np.triu(np.ones_like(data_n.corr(),dtype = bool))
    # heatmap = sns.heatmap(data_n.corr(), mask=mask, vmin=-1, vmax=1, center=0, annot=False, cmap="Set2")
    # heatmap.set_title('Correlation Heatmap', pad=12)
    # plt.show()

    # Correlation matrix
    
    
    data_num = data[numerical_features]
    data_num_mod = data_num.drop(['step','isFlaggedFraud'],axis=1)
    corr = data_num_mod.corr()
    plt.figure(figsize = (6,4))
    mp = sns.heatmap(corr, linewidth = 1 ,vmin=-1, vmax=1, center=0,  annot=True, cmap="coolwarm", fmt=".2f")
    plt.show()

    #count plot 
    # sns.set_style('whitegrid')
    # sns.set_context('notebook')
    # plt.figure(figsize=(8, 4))
    # counplot = sns.countplot(data=data, x='type', hue='isFraud',palette= "pastel")
    # counplot.set_xlabel('Type ')
    # counplot.set_ylabel(f'count')
    # counplot.set_yscale('log')
    # counplot.yaxis.set_major_formatter(mticker.ScalarFormatter())
    # plt.show()

    #histogram plot
    # plt.figure(figsize=(10, 6))
    # palette = sns.color_palette("pastel")
    # histplot = sns.histplot(data=data[:100000], 
    #                         x='amount', 
    #                         hue='isFraud', 
    #                         kde=True, 
    #                         element='step', 
    #                         palette= "Set2", 
    #                         log_scale=True)
    # histplot.set_ylabel('Number of Observations')
    # histplot.set_xlabel(f'amount')
    # mean_value_f = data[data['isFraud']==False]['amount'].mean()
    # mean_value_t = data[data['isFraud']==True]['amount'].mean()
    # histplot.axvline(x=mean_value_f, color=palette[0])
    # histplot.axvline(x=mean_value_t, color=palette[-1])
    # histplot.annotate(f'Mean amount for regular transactions: ${mean_value_f:,.2f}', 
    #                   xy=(0.1, 0.5),
    #                   xycoords='axes fraction')
    # histplot.annotate(f'Mean amount for fraudulent transactions: ${mean_value_t:,.2f}', 
    #                   xy=(0.1, 0.3),
    #                   xycoords='axes fraction')
    # histplot.xaxis.set_major_formatter(mticker.ScalarFormatter())
    # histplot.ticklabel_format(style='plain', 
    #                           axis='x')  
    # plt.show()
    

    # visualisation of categorical_features
    # for categorical_column in categorical_features:
    #     fig, axs = plt.subplots(figsize=(5,5))
    #     sns.countplot(data=data, x=categorical_column)
    #     plt.show()
    #Distrubution of numerical features
    for numerical_feature in numerical_features:
        fig, axs = plt.subplots(figsize=(5,4))
        sns.distplot(data[numerical_feature])
        plt.xlabel(numerical_feature)
        plt.show()
    #finding outliers in numerical features
    for numerical_feature in numerical_features:
        fig, axs = plt.subplots(figsize=(7,5))
        sns.boxplot(data[numerical_feature])
        plt.xlabel(numerical_feature)
        plt.show()
       
    return data 

visualise_data()