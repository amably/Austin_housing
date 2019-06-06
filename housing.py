def process_csv(metro):
    '''
    Function to process csv files from Zillow.com.
    Reads in files from a 'raw' folder, and saves 
    resulting csvs in 'clean' folder.
    '''    

    import pandas as pd
    import numpy as np
    import pathlib
    
    def filter_and_transpose(df, metro):
        '''
        Function to select the metro area of interest from the Zillow.com csv.
        And transpose the dataframe to give a datetime index
        '''
        #filter metro area of interest
        df0 = df[df['Metro']==metro]
        
        #clean and transpose dataframe
        df0 = df0.drop(columns = ['RegionID','City','State','Metro','CountyName','SizeRank'])
        df0 = df0.rename(index=str, columns={'RegionName': 'Zipcode'})
        df0 = df0.T
        df0.columns = df0.iloc[0].astype(int).astype(str)
        df0 = df0.copy()[1:]
        
        #convert index to datetime index
        df0.index = pd.to_datetime(df0.index)
        
        #standardize amounts to thousands of $$
        df0 = df0.astype(float)/1000
        
        return df0
        
        
    open_directory = pathlib.Path('zip_data/raw')
    save_directory = 'zip_data/clean/'
    
    for csv in open_directory.glob('*.csv'):
        #load file
        df = pd.read_csv(csv, encoding = "ISO-8859-1")
        
        #pass file to function to clean and process df
        p_df = filter_and_transpose(df, metro)
        
        #save resulting df in 'clean' folder
        save_file = (save_directory + str(csv)[17:-4] + metro + '_clean.csv')        
        p_df.to_csv(save_file)

