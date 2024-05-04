import sqlite3
import pandas as pd
import os,sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import adjust_date
from infodata import features, reference_day_esios, reference_hour_esios
import ESIOS
import mibgas
from load_historic_data import load_esios_data


def max_date_time_esios(item = 'demand'):
    
    # Connect to the SQLite database 
    conn = sqlite3.connect('Main_DB')

    # SQL query for date
    max_date = f'''
    SELECT max(day) from {item}
    '''

    # Execute query
    last_date = pd.read_sql_query(max_date, conn).iloc[0, 0]

    # Add exception for empty ddbb
    if last_date == None:
        print('Data could not be retrieved, using reference date')
        return reference_day_esios, reference_hour_esios
    
    # SQL query for date
    max_hour = f'''
    SELECT max(hour) from {item}
    WHERE day = '{last_date}'
    '''

    # Execute query
    last_hour = pd.read_sql_query(max_hour, conn).iloc[0, 0]

    # Close the connection
    conn.close()

    return last_date, last_hour


def max_date_time_mibgas(item = 'gas_data'):
    
    # Connect to the SQLite database 
    conn = sqlite3.connect('Main_DB')

    # SQL query for date
    max_date = f'''
    SELECT max(delivery_day) from {item}
    '''

    # Execute query
    last_date = pd.read_sql_query(max_date, conn).iloc[0, 0]

    # Close the connection
    conn.close()

    return last_date

def update_datasets(feature):
    from datetime import datetime


    # Get last date
    last_day_esios, last_hour_esios = max_date_time_esios(feature)
    last_day_mibgas = max_date_time_mibgas()
    
    # Update date
    last_day_esios_updated = adjust_date(last_day_esios, last_hour_esios)

    # Get current date
    #data has to be on the form "2019-01-01T00:00:00"
    current_date_time_esios = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    current_date_time_mibgas = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Update dataset
    load_esios_data(last_day_esios_updated, current_date_time_esios, feature)

    # Confirmation Message (including first and last dates of the dataset and count)
    #Confirmation

    #First and last dates

    #Total count
    pass

if __name__ == "__main__":
    for feature in features:
        update_datasets(feature)