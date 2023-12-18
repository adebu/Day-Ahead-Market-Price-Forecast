import pandas as pd
import requests
import sqlite3

def get_training_data(start_date, end_date, inputs):
    '''
    Download data from ESIOS API considering dates and specified demand.
    '''

    urls = {
        "demand": f"https://api.esios.ree.es/indicators/1775?type=3&start_date={start_date}&end_date={end_date}",
        "wind": f"https://api.esios.ree.es/indicators/1777?type=20&start_date={start_date}&end_date={end_date}",
        "solar": f"https://api.esios.ree.es/indicators/1779?type=3&start_date={start_date}&end_date={end_date}",
        "spot_price": f"https://api.esios.ree.es/indicators/602?type=3&start_date={start_date}&end_date={end_date}"
    }
    try:

        url = urls[inputs]

        # headers for the API
        headers = dict()
        headers['Accept'] = 'application/json; application/vnd.esios-api-v1+json'
        headers['Content-Type'] = 'application/json'
        headers['Host'] = 'api.esios.ree.es'
        headers['x-api-key'] = "27ac7b794ca773e7d1c6ea0f43adfd466abe7dbd6682b769ddd29cf25536c1d6"
        headers['Cookie'] = ''

        # connect to the API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
        else:
            print("Error: Request failed with status code", response.status_code)

        return data

    except:

        print("could not retrieve data")


def extract_values(data, call_data):
    '''
    Extracts values and time from the ESIOS data and returns a Pandas DataFrame.
    '''
    #values = [v["value"] for v in data["indicator"]["values"]]
    #times = [v["datetime"] for v in data["indicator"]["values"]]
    try:
        values = data["indicator"]["values"]
        df = pd.DataFrame(values)
        return df
    except:
        print(f'No values could be extracted for {call_data}')
    # Create a DataFrame with 'time' and 'call_data' columns
    #df = pd.DataFrame({ 'time': times, call_data: values })



def connection_to_DB(df, call_data):
    '''
    Calls marginal_to_df and loads the df into a SQLite db
    '''

    try:


        conn = sqlite3.connect('Main_DB')
        c = conn.cursor()
        '''
        # Creates table to store marginalpdbc
        c.execute(f''''''CREATE TABLE IF NOT EXISTS {call_data} (
                year number, 
                month number, 
                day number, 
                hour number, 
                price_ES number, 
                price_PT number,
                PRIMARY KEY (year, month, day, hour)
                )
                '''''')
        conn.commit()
        '''
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
        print('Data uploaded succesfully')



    except Exception as e:
        print("Could not upload the data to the DB")
        print(e)