import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(1, parent_dir)

from infodata import start_date, features


def merge_df (wind, spot_price, solar, demand, nuclear, gas_data):
    """
    Merge multiple dataframes representing different energy sources and demand data 
    with gas delivery data based on specified columns 'day' and 'hour', creating a unified dataframe.

    Parameters:
    - wind: DataFrame representing wind energy data with columns 'day' and 'hour'.
    - spot_price: DataFrame representing spot price data with columns 'day' and 'hour'.
    - solar: DataFrame representing solar energy data with columns 'day' and 'hour'.
    - demand: DataFrame representing energy demand data with columns 'day' and 'hour'.
    - nuclear: DataFrame representing nuclear energy data with columns 'day' and 'hour'.
    - gas_data: DataFrame representing gas delivery data with a column 'delivery_day'.

    Returns:
    - df: Merged DataFrame containing data from all input sources, with columns joined based on 'day' and 'hour'.
          The 'delivery_day' column from gas_data is dropped after merging.
    """

    df=wind.merge(spot_price, left_on=['day', 'hour'], right_on=['day', 'hour']) \
        .merge(solar, left_on=['day', 'hour'], right_on=['day', 'hour']) \
        .merge(demand, left_on=['day', 'hour'], right_on=['day', 'hour']) \
        .merge(nuclear, left_on=['day', 'hour'], right_on=['day', 'hour']) \
        .merge(gas_data, left_on=['day'], right_on=['delivery_day'])\
        .drop('delivery_day', axis=1)
    
    return df
    
def clean_dataset():
    '''
    '''
    pass


def query_values(features, first_date = start_date):
    try:
        # Connect to the SQLite database (if the database doesn't exist, it will be created)
        conn = sqlite3.connect('Main_DB')

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Your SQL query
        temp_df = '''
        SELECT * from wind
        '''

        # Read SQL query result into a DataFrame
        wind = pd.read_sql_query(temp_df, conn)
        wind.rename(columns={'value': 'wind_generation'}, inplace=True)

        # Your SQL query
        temp_df = '''
        SELECT * from spot_price
        '''

        # Read SQL query result into a DataFrame
        spot_price = pd.read_sql_query(temp_df, conn)

        # Read SQL query result into a DataFrame
        spot_price = pd.read_sql_query(temp_df, conn)
        spot_price.rename(columns={'value': 'spot_price'}, inplace=True)

        # Your SQL query
        temp_df = '''
        SELECT * from solar
        '''

        # Read SQL query result into a DataFrame
        solar = pd.read_sql_query(temp_df, conn)
        solar.rename(columns={'value': 'solar_generation'}, inplace=True)

        # Your SQL query
        temp_df = '''
        SELECT * from demand
        '''

        # Read SQL query result into a DataFrame
        demand = pd.read_sql_query(temp_df, conn)
        demand.rename(columns={'value': 'demand'}, inplace=True)

        # Your SQL query
        temp_df = '''
        SELECT * from nuclear
        '''

        # Read SQL query result into a DataFrame
        nuclear = pd.read_sql_query(temp_df, conn)
        nuclear.rename(columns={'value': 'nuclear_generation'}, inplace=True)

        # SQL query
        temp_df = '''
        SELECT * from gas_data
        '''

        # Read SQL query result into a DataFrame
        gas_data = pd.read_sql_query(temp_df, conn)
        gas_data.rename(columns={'value': 'gas_price'}, inplace=True)
        gas_data_hourly = gas_data.reindex(gas_data.index.repeat(24)).reset_index(drop=True)

        # Close the connection
        conn.close()

        df = merge_df(wind, spot_price, solar, demand, nuclear, gas_data)

        return df
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
        # Log the error here







if __name__ == "__main__":
    for feature in features:
        update_datasets(feature)