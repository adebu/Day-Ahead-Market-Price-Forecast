


def get_generation_data(start_date, end_date, inputs):
    '''
    Download data from ESIOS API considering dates and specified technology.
    '''
    import requests

    urls = {
        "wind": f"https://api.esios.ree.es/indicators/541?type=3&start_date={start_date}&end_date={end_date}",
        "hydro": f"https://api.esios.ree.es/indicators/211?type=20&start_date={start_date}&end_date={end_date}",
        "solar": f"https://api.esios.ree.es/indicators/530?type=3&start_date={start_date}&end_date={end_date}",
        "nuclear": f"https://api.esios.ree.es/indicators/540?type=3&start_date={start_date}&end_date={end_date}",
        "marginal_price": f"https://api.esios.ree.es/indicators/101?type=3&start_date={start_date}&end_date={end_date}"
    }

    # Use the especified URL to get the low cost generation
    try:
        url = urls[inputs]
    except:
        print("Input does not exist")

    # Get the correct format for the date
    #start_date = date_format(start_date)
    #end_date = date_format(end_date)

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


import pandas as pd

def extract_values(data, call_data):
    '''
    Extracts values and time from the ESIOS data and returns a Pandas DataFrame.
    '''
    values = [v["value"] for v in data["indicator"]["values"]]
    times = [v["datetime"] for v in data["indicator"]["values"]]

    # Create a DataFrame with 'time' and 'call_data' columns
    df = pd.DataFrame({ 'time': times, call_data: values })

    return df