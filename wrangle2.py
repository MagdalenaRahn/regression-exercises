## IMPORTS

import os

import pandas as pd

from pydataset import data

from env import host, username, password, sql_connexion

## FUNCTION TO CONNECT TO THE MYSQL SERVER

def sql_connexion(db_name):
    
    '''
    This function connects to the SQL database,
    allowing for the retrieval of remote data.
    '''
    from env import host, username, password
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'

def get_zillow_data():
    '''
    This function reads in the Zillow data from the Codeup db
    and returns a pandas DataFrame with cbedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, and fips
    for all Single Family Residential properties.
    '''
    
    zillow_query = '''
    SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    FROM properties_2017
    WHERE propertylandusetypeid = 261
    '''
    return pd.read_sql(zillow_query, sql_connexion('zillow'))

  
def prep_zillow(df):
    '''
    This function will use the imported
    zillow_single_family_properties_2017.csv, 
    drop any NaN or null values, rename columns 
    to be more legible, and drop superfluous 
    ones ('propertylandusetypeid' and 'Unnamed: 0'),
    returning  the whole to a cleaned DataFrame.
    '''  
    #change column names to be more readable
    df = df.rename(columns={'bedroomcnt':'bedrooms', 
                          'bathroomcnt':'bathrooms', 
                          'calculatedfinishedsquarefeet':'area',
                          'taxvaluedollarcnt':'tax_value', 
                          'yearbuilt':'year_built'})

    # dropping unnecessary columns 'propertylandusetypeid' and 'Unnamed: 0'
    df = df.drop(columns = ['propertylandusetypeid', 'Unnamed: 0'], axis = 0)

    #drop null values- at most there were 9000 nulls (this is only 0.5% of 2.1M)
    df = df.dropna()

    #drop duplicates
    df.drop_duplicates(inplace=True)
    
    # train/validate/test split
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    
    return train, validate, test


def wrangle_zillow():
    '''
    this function will acquire, prepare and split
    the zillow data in one function.
    '''
    train, validate, test = prep_zillow(get_zillow_data())
    
    return train, validate, test




    
