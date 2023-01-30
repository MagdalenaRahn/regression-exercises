## IMPORTS

import os

import pandas as pd

from pydataset import data

from env import host, username, password, sql_connexion

from sklearn.model_selection import train_test_split



def prep_zillow(zil):
    
    '''
    This function will use the imported
    ************   zillow_single_family_properties_2017.csv, 
    drop any NaN or null values, rename columns 
    to be more legible, and drop superfluous 
    ones ('parcelid') and outliers,
    returning the whole to a cleaned DataFrame.
    '''  
    
    #change column names to be more readable
    zil = zil.rename(columns = {'bedroomcnt' : 'num_br', 
                                'bathroomcnt' : 'num_ba', 
                                'calculatedfinishedsquarefeet' : 'total_sqft', 
                                'transactiondate' : 'date_sold', 
                                'taxvaluedollarcnt' : 'tax_val', 
                                'fips' : 'county_fips'})

    # dropping unnecessary columns 'propertylandusetypeid' and 'Unnamed: 0'
    zil = zil.drop(columns = ['Unnamed: 0','date_sold','parcelid'], axis = 0)
    
    # casting the FIPS column as an integer
    zil = zil.astype({'county_fips':'int64'})
    
    # filling na spaces with 0
    zil = zil.fillna(0)
    
    # dropping houses with 0 sq ft
    zil = zil[zil.total_sqft > 0]

    # dropping houses with 0 bathrooms
    zil = zil[zil.num_ba > 0]

    # dropping houses with 0 tax value
    zil = zil[zil.tax_val > 0]
    
    # dropping houses with a tax value of more than $2 mil
    zil = zil[zil.tax_val <= 2_000_000]
    
    #drop duplicates
    zil.drop_duplicates(inplace = True)
    
    return zil





# Fuction to split data into train, validate, split

def tts_zillow(zil):
    
    '''
    this function splits the prepared Zillow data 
    into train, validate and test
    '''

    # train/validate/test split
    train_val, test = train_test_split(zil, test_size = 0.2, random_state = 23)
    train, val = train_test_split(train_val, test_size = 0.3, random_state = 23)
    
    return train, val, test





# Function to split train, validate and test into Xs and ys
# it has not yet been tested in its current form

# train, validate, test are retrieved from the 'tts_zillow(zil)' function.
# the target needs to be entered in quotes, i.e, 'target_variable'.

def tts_xy(train, val, test, target):
    
    '''
    This function splits train, val, test into X_train, X_val, X_test
    (the dataframe of features, exludes the target variable) 
    and y-train (target variable), etc
    '''

    X_train = train.drop(columns = [target])
    y_train = train[target]


    X_val = val.drop(columns = [target])
    y_val = val[target]


    X_test = test.drop(columns = [target])
    y_test = test[target]

    return X_train, y_train, X_val, y_val, X_test, y_test




## A GENERIC FUNCTION TO TRAIN, TEST AND SPLIT DATA.

def my_train_test_split(df, target):
    
    '''
    This is an alternate, generic function serving to split data 
    into training, validating and testing groups, allowing for 
    machine learning-training to be undertaken.
    '''
    
    train, test = train_test_split(df, test_size = .2, 
                                   random_state = 123, 
                                   stratify = df[target])
    
    train, validate = train_test_split(train, test_size = .25, 
                                       random_state = 123, 
                                       stratify = train[target])
    
    return train, validate, test


