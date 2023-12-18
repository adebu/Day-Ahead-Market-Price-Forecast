import pandas as pd
import requests
import os

class ESIOS:
    def __init__(self):
        #define API parameters
        pass
    
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
