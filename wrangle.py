import os

## FUNCTION TO CONNECT TO THE MYSQL SERVER

def sql_connexion(db, user = username, host = host, password = password):
    
    '''
    This function connects to the SQL database,
    allowing for the retrieval of remote data.
    '''
    
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

    
    
    
    
    
## FUNCTION TO WRANGLE THE ZILLOW SINGLE-FAMILY HOMES 2017 DATA

def wrangle_zillow_sfh_2017():
    
    '''
    This function will use the imported
    zillow_single_family_properties_2017.csv, 
    drop any NaN or null values, rename columns 
    to be more legible, and drop superfluous 
    ones ('propertylandusetypeid' and 'Unnamed: 0'),
    returning  the whole to a cleaned DataFrame.
    '''
    
    # acquire the data
    zil = get_zillow_data()
    
    # drop null values
    zil = zil.dropna()
    
    # # rename unsightly column names
    zil = zil.rename(columns = {'bedroomcnt' : 'num_br', 
                                'bathroomcnt' : 'num_ba', 
                                'calculatedfinishedsquarefeet' : 'total_sqft', 
                                'taxamount' : 'taxes', 
                                'taxvaluedollarcnt' : 'current_tax_val', 
                                'yearbuilt' : 'year_built'})
    
    # dropping unnecessary columns 'propertylandusetypeid' and 'Unnamed: 0'
    zil = zil.drop(columns = ['propertylandusetypeid', 'Unnamed: 0'], axis = 0)
    
    return df
  
    