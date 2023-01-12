## IMPORTS

import os

import pandas as pd

from pydataset import data

from sklearn.model_selection import train_test_split

from env import host, username, password, sql_connexion



  
def prep_zillow(zil):
    '''
    This function will use the imported
    zillow_single_family_properties_2017.csv, 
    drop any NaN or null values, rename columns 
    to be more legible, and drop superfluous 
    ones ('propertylandusetypeid' and 'Unnamed: 0'),
    returning  the whole to a cleaned DataFrame.
    '''  
    #change column names to be more readable
    zil = zil.rename(columns = {'bedroomcnt':'nº_br', 
                          'bathroomcnt':'nº_br', 
                          'calculatedfinishedsquarefeet':'area_sqft',
                          'taxvaluedollarcnt':'tax_value',
                          'taxamount':'tax_amount',
                          'yearbuilt':'year_built'})

    # dropping unnecessary columns 'propertylandusetypeid' and 'Unnamed: 0'
    zil = zil.drop(columns = ['propertylandusetypeid', 'Unnamed: 0'], axis = 0)

    #drop null values- at most there were 9000 nulls (this is only 0.5% of 2.1M)
    zil = zil.dropna()

    #drop duplicates
    zil.drop_duplicates(inplace = True)
    
    # train/validate/test split
    train_validate, test = train_test_split(zil, test_size = 0.2, random_state = 23)
    train, validate = train_test_split(train_validate, test_size = 0.3, random_state = 23)
    
    return train, validate, test


def wrangle_zillow(zil):
    '''
    this function will acquire, prepare and split
    the zillow data in one function.
    '''
    train, validate, test = prep_zillow(zil)
    
    return train, validate, test




    
