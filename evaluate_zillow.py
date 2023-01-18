'''
Create a file named evaluate.py that contains the following functions.

    plot_residuals(y, yhat): creates a residual plot
    regression_errors(y, yhat): returns the following values:

      - sum of squared errors (SSE)
      - explained sum of squares (ESS)
      - total sum of squares (TSS)
      - mean squared error (MSE)
      - root mean squared error (RMSE)

    baseline_mean_errors(y): computes the SSE, MSE, and RMSE for the baseline model
    better_than_baseline(y, yhat): returns true if your model performs better than the baseline, otherwise false
'''

# imports

import os

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.model_selection import train_test_split


# import my functions
import wrangle_no_acquire
import explore_zillow_sfh_2017

from env import host, username, password, sql_connexion


## make a scatter plot of the model's prediction minus the actual preditcion of tax_value

def plot_residuals(y, yhat):
    
    '''
    This function makes a scatter plot of the model's prediction 
    minus the actual prediction of tax_value against the yhat residuals.
    '''
    
    plt.scatter(y, yhat)

    plt.xlabel('Tax Value')
    plt.ylabel('Predictions Residual')
    plt.show()
    
    
    
def regression_errors(y, yhat, df): 
    
    '''
    This function returns the following values:
      - sum of squared errors (SSE)
      - explained sum of squares (ESS)
      - total sum of squares (TSS)
      - mean squared error (MSE)
      - root mean squared error (RMSE)
     '''
    
    # calculate SSE
    # square the columns of interest to find baseline residuals sqaured and the yhat residuals squared
    df['baseline_residual_squared'] = df['baseline_residual'] ** 2
    df['yhat_residual_squared'] = df['yhat_residual'] ** 2


    # find the total amount of error 
    total_error = df['baseline_residual_squared'].sum()

    # sum of squared error baseline as a variable
    sse_baseline = df['baseline_residual_squared'].sum()

    # sum of squared error yhat
    sse_yhat = df['yhat_residual_squared'].sum()
    
    # find the baseline MSE
    mse_baseline = sse_baseline / len(df)
    
    # find the MSE of yhat
    mse_yhat = sse_yhat / len(df)
    
    # establishing ess baseline as 0.
    # calculating the TSS baseline
    ess_baseline = 0
    tss_baseline = sse_baseline + ess_baseline

    # make new column in preds, for yhat only, because it would not results in a 0
    df['yhat_mean_residual'] = df['yhat'] - df['baseline_predictions']

    # now we need to square each diffrence
    # looking at differenc between predictions and baseline
    df['yhat_mean_residual_squared'] = df['yhat_mean_residual'] ** 2

    # calulating the ess_yhat
    ess_yhat = df['yhat_mean_residual_squared'].sum()

    # calculating the TSS yhat
    tss_yhat = sse_yhat + ess_yhat

    # square root of baseline
    rmse_baseline = sqrt(mse_baseline)

    # square root of yvalue
    rmse_yhat = sqrt(mse_yhat)
    
    return sse_baseline, sse_yhat, mse_baseline, mse_yhat, ess_baseline, tss_baseline, ess_yhat, tss_yhat, rmse_baseline, rmse_yhat
