import requests
import pandas as pd
import json


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