import pandas as pd
import requests
import os
import sqlite3
from private_info import headers
import os
import sys
# Getting the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Moving one directory back
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Inserting the path to sys.path
sys.path.insert(1, parent_dir)
from utils import adjust_timestamp

class ESIOS:
    def __init__(self):
        #define API parameters
        pass
    
    def get_training_data(start_date, end_date, inputs):
        '''
        Download data from ESIOS API considering dates and specified demand.
        '''
        if inputs == 'spot_price':
            appendix = '&geo_ids[]=3'
        else:
            appendix = ''

        indicators ={'demand':1775, 'wind':1777, 'solar': 1779, 'spot_price': 600}
        
        url = f"https://api.esios.ree.es/indicators/{indicators[inputs]}?start_date={start_date}&end_date={end_date}{appendix}"
           
        try:

            # connect to the API
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # Process the data as needed
            else:
                print("Error: Request failed with status code", response.status_code)

            return data

        except Exception as e:

            print("could not retrieve data")
            print(e)
    

    def extract_values(data, call_data):
        '''
        Extracts values and time from the ESIOS data and returns a Pandas DataFrame.
        '''
        #values = [v["value"] for v in data["indicator"]["values"]]
        #times = [v["datetime"] for v in data["indicator"]["values"]]
        try:
            values = data["indicator"]["values"]
            df = pd.DataFrame(values)
            

            # adjust for timezone
            df = adjust_timestamp(df)

            df = df[['value','datetime']]

            # datetime in the form 2019-01-01T00:00:00.000+01:00
            df[['day', 'hour']] = df['datetime'].str.split(' ', expand=True)

            # remove hour references
            df['hour'] = df['hour'].str[:5]

            # remove unnecesary column
            df = df.drop('datetime', axis=1)

            return df
        
        except Exception as e:
            print(f'No values could be extracted for {call_data}')
            print(e)
        # Create a DataFrame with 'time' and 'call_data' columns
        #df = pd.DataFrame({ 'time': times, call_data: values })

    def create_indicators_file ():

        if os.path.isfile("filename.txt"):
            print('The indicators file is already created!')


        else:
            try:    
                indicators = "https://api.esios.ree.es/indicators"
                headers = dict()
                headers['Accept'] = 'application/json; application/vnd.esios-api-v1+json'
                headers['Content-Type'] = 'application/json'
                headers['Host'] = 'api.esios.ree.es'
                headers['x-api-key'] = "27ac7b794ca773e7d1c6ea0f43adfd466abe7dbd6682b769ddd29cf25536c1d6"
                headers['Cookie'] = ''

                # connect to the API
                response = requests.get(indicators, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    # Process the data as needed
                else:
                    print("Error: Request failed with status code", response.status_code)

                df = pd.DataFrame(data["indicators"])
                df.to_csv('indicators.csv')
                print('Indicators file created succesfully!')
            except Exception as e:
                print('Indicators file could not be created')
                print(e)

    def connection_to_DB(df, call_data, year):
        '''
        Calls marginal_to_df and loads the df into a SQLite db
        '''

        try:


            conn = sqlite3.connect('Main_DB')
            c = conn.cursor()
            
            # Creates table to store marginalpdbc
            c.execute(f'''CREATE TABLE IF NOT EXISTS {call_data} (
                    value number, 
                    day date, 
                    hour string
                    )
                    ''')
            conn.commit()
        
            # Send dataframe to db
            df.to_sql(f'{call_data}', conn, if_exists='append', index=False,
                    method='multi', chunksize=1000)
            '''
            # Check for duplicates in the
            c.execute(f''''''
            DELETE FROM {call_data}
            WHERE ROWID NOT IN (
            SELECT MIN(ROWID) FROM {call_data}
            GROUP BY year, month, day, hour)
            '''''')
            '''
            print(f'{len(df)} {call_data} data values uploaded succesfully for year {year[0:4]} ')



        except Exception as e:
            print("Could not upload the data to the DB")
            print(e)