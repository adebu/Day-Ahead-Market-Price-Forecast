import sqlite3
import pandas as pd

def upload_esios(item):
    
    # Connect to the SQLite database 
    conn = sqlite3.connect('Main_DB')

    # SQL query
    temp_df = f'''
    SELECT max(day) from {item}
    '''
    
    last_date = pd.read_sql_query(temp_df, conn)

    # Close the connection
    conn.close()

    return last_date


def upload_gas():
    pass

test = upload_esios('demand')
test