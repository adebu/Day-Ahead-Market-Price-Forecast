import requests
from io import BytesIO
import pandas as pd
import openpyxl
import io

class mibgas:
    
    def __init__(self):
        pass

    def get_data(year):
        
        try:
            url = f'https://www.mibgas.es/es/file-access/MIBGAS_Data_{year}.xlsx?path=AGNO_{year}/XLS'

            # GET request to the URL
            response = requests.get(url)

            if response.status_code == 200:
                # Load the content of the XLSX file into a BytesIO buffer
                file_content = io.BytesIO(response.content)
                
                # Read the XLSX file using openpyxl
                workbook = openpyxl.load_workbook(file_content)
                
                # Get the names of all sheets in the workbook
                indexes = workbook['MIBGAS Indexes']

                data = indexes.values
                
                data_list = list(data)
                df = pd.DataFrame(data_list[1:], columns=data_list[0])
                
                # drop nan columns by date
                df = df.dropna(subset=['Delivery day'])
                
                return df  # Return the list of sheet names
            else:
                print('Failed to retrieve the information from MIBGAS websitewebpage. Status code:', response.status_code)
                return None

        except Exception as e:
            print(f'An error occured while loading gas data: {e}')

    def extract_data(gas_data):
        pass

test = mibgas.get_data(2023)
print(test)