import requests
import pandas as pd
import sqlite3
import openpyxl
import io

class mibgas:
    
    def __init__(self):
        pass

    def get_data(year):
        
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
            print('Failed to retrieve the webpage. Status code:', response.status_code)
            return None

    def adapt_data (df):
        
        df = df.rename(columns={"Delivery day": "delivery_day",
                                 "MIBGAS PVB Last Price Index Day-Ahead\n[EUR/MWh]": "PVB_last_price",
                                 "MIBGAS PVB Average Price Index Day-Ahead\n[EUR/MWh]": "PVB_avg_price",
                                 "MIBGAS VTP Last Price Index Day-Ahead\n[EUR/MWh]": "VTP_last_price",
                                 "MIBGAS VTP Average Price Index Day-Ahead\n[EUR/MWh]": "VTP_avg_price",
                                 "MIBGAS-ES Index\n[EUR/MWh]": "index_ES",
                                 "MIBGAS-PT Index\n[EUR/MWh]": "index_PT",
                                 "MIBGAS\nLNG-ES Index\n[EUR/MWh]": "LNG_ES",
                                 "MIBGAS\nLNG-ES Index\n[EUR/MWh]": "LNG_PT",
                                 "MIBGAS\nAVB-ES Index\n[EUR/MWh]": "AVB_ES"                                 
                                 })
        
        
        return df
    
    def connection_to_DB(df):
        '''
        Calls marginal_to_df and loads the df into a SQLite db
        '''

        try:


            conn = sqlite3.connect('Main_DB')
            c = conn.cursor()
            
            # Creates table to store gas data
            c.execute(f'''CREATE TABLE IF NOT EXISTS gas_data (
                    delivery_day date, 
                    PVB_last_price number, 
                    PVB_avg_price number, 
                    VTP_last_price number, 
                    VTP_avg_price number, 
                    index_ES number,
                    index_PT number,
                    LNG_ES number,
                    LNG_PT number,
                    AVB_ES number,
                    PRIMARY KEY (delivery_day)
                    )
                    ''')
            conn.commit()
            df.to_sql('gas_data', conn, if_exists='replace', index=False,
                  method='multi', chunksize=1000)
            # Send dataframe to db
            print('Data uploaded succesfully')



        except Exception as e:
            print("Could not upload the data to the DB")
            print(e)


if __name__ == "__main__":
    
    years = [2023]

    for year in years:
        gas_data = mibgas.get_data(year)
        gas_data_cleaned = mibgas.adapt_data(gas_data)
        mibgas.connection_to_DB(gas_data_cleaned)
