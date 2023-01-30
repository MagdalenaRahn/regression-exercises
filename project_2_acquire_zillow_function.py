## IMPORTS

import os

import pandas as pd

from pydataset import data

from env import host, username, password, sql_connexion





## FUNCTION TO CONNECT TO THE MYSQL SERVER

def sql_connexion(db, user = username, host = host, password = password):
    
    '''
    This function connects to the SQL database,
    allowing for the retrieval of remote data.
    '''
    
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
    
    
    
## FUNCTION TO ACQUIRE THE ZILLOW DATASET FROM SQL
    

def get_zillow_2017_data(zil):
    
    '''
    This function retrieves Zillow 2017 single-family homes 
    that had a transaction from a .csv, if the .csv is 
    held locally, or pulls it from SQL in the case that 
    it's held remotely.
    '''
    
    if os.path.isfile('file.csv'):
        
        return pd.read_csv('file.csv')
    
    else:
        
        url = zil('zillow')
    
        query = '''
        SELECT parcelid, transactiondate, bathroomcnt, bedroomcnt, 
            calculatedfinishedsquarefeet, fips, taxvaluedollarcnt
        FROM properties_2017
        JOIN predictions_2017 
            USING(parcelid)
        JOIN propertylandusetype 
            USING(propertylandusetypeid)
        WHERE propertylandusetypeid = 261;
                '''
        zil = pd.read_sql(query, url)
        
        zil.to_csv('zillow_sfh_2017_sold.csv')
        
    return zil