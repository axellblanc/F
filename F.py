#! usr/bin/python3


# Functions for the F.ipynb notebook

from datetime import datetime 
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.dates as mdates



def get_returns(df_price):
    """
    Returns from the asset
    Arguments:
        df_price {pd.DataFrame} -- DataFrame with the prices over a period
    Returns:
        pd.DataFrame -- the returns
    """
    returns = df_price.pct_change(1)
    return returns.dropna()

def get_log_returns(df):
    """
    Log returns from the asset
     Arguments:
        df_price {pd.DataFrame} -- DataFrame with the prices over a period
    Returns:
        pd.DataFrame -- the log returns
    """
    log_returns = np.log(df).diff()
    return log_returns.dropna()


def get_portfolio_returns(weights_matrix, df_price):
    """
    Log returns from the portfolio
     Arguments:
        df_price {pd.DataFrame} -- DataFrame with the prices over a period
        weights_matrix {pd.DataFrame} -- DataFrame with the weights of the portfolio
    Returns:
        pd.DataFrame -- the log returns
    """
    log_returns = get_log_returns(df_price)
    temp_var = weights_matrix.dot(log_returns.transpose())
    return pd.Series(np.diag(temp_var), index=log_returns.index)




def plot_returns(df, name = ''):
    """
    Plots the returns from one or many stock
     Arguments:
        df {pd.DataFrame} -- DataFrame with the prices over a period
        name {string} -- name of the stock if it is contained in a pd.series
    """
    print('\n\n Cummulative returns and log returns: \n \n')
    returns = get_returns(df)
    log_returns = get_log_returns(df)
    
    if isinstance(df, pd.Series):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16,12))
        ax1.plot(log_returns.index, log_returns.cumsum(), label=str(name), color = 'blue')
        ax1.set_ylabel('Cumulative log returns')
        ax1.legend(loc='best')
        ax2.plot(log_returns.index, (np.exp(log_returns.cumsum()) - 1), label=str(name), color = 'red')
        ax2.set_ylabel('Total relative returns (%)')
        ax2.legend(loc='best')
        plt.show()
    
    else:
        plt.figure(figsize=(16,6))
        for ticker in returns.columns:   
            plt.plot(log_returns.index, log_returns[ticker].cumsum(), label=ticker)
            plt.ylabel('Cumulative log returns')
            plt.legend(loc='best')
        plt.figure(figsize=(16,6))
        for ticker in returns.columns: 
            plt.plot(log_returns.index, (np.exp(log_returns[ticker].cumsum()) - 1), label=ticker)
            plt.ylabel('Total relative returns (%)')
            plt.legend(loc='best')
        plt.show()
    

    
    

def plot_rollings(df, windows, name = ''):
    """Plots the rolling means of df which sizes are included in windows 
    Plot the returns from one or many stock
     Arguments:
        df {pd.DataFrame} -- DataFrame with the prices over a period
        windows {list} -- length of the windows of the rolling means to print
    """

    fig, ax = plt.subplots(figsize=(16,9))
    plt.plot(df.index, df, label=name, color = 'blue')
    for w in windows:
        rolling = df.rolling(window=w).mean()
        ax.plot(rolling.index, rolling, label= str(w)+' days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()
    
    
    
    
def print_portfolio_yearly_statistics(portfolio_cumulative_relative_returns, days_per_year = 52 * 5):

    total_days_in_simulation = portfolio_cumulative_relative_returns.shape[0]
    number_of_years = total_days_in_simulation / days_per_year

    # The last data point will give us the total portfolio return
    total_portfolio_return = portfolio_cumulative_relative_returns[-1]
    # Average portfolio return assuming compunding of returns
    average_yearly_return = (1 + total_portfolio_return)**(1/number_of_years) - 1

    print('Total portfolio return is: ' + '{:5.2f}'.format(100*total_portfolio_return) + '%')
    print('Average yearly return is: ' + '{:5.2f}'.format(100*average_yearly_return) + '%')


    
    
    
