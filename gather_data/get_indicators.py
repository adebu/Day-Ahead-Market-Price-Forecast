import requests
import pandas as pd
import os


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
