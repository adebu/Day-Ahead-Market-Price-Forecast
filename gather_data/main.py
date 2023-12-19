from downloadFiles import get_training_data, extract_values, connection_to_DB
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ESIOS import ESIOS
from mibgas import mibgas

# load data from ESIOS since 2019

start_date = "2019-01-01T00:00:00"
end_date = "2023-01-01T00:00:00"

training_data = ['demand', 'wind', 'solar', 'spot_price']
historic_data = ['demand_historic', 'wind_historic', 'solar_historic']

# convert start_date and end_date to datetime objects
start_date = datetime.fromisoformat(start_date)
end_date = datetime.fromisoformat(end_date)
current_date = start_date

while current_date < end_date:
    # calculate the end of the current month
    query_year = current_date+ relativedelta(years = 1)

    # format end_of_month in the "%Y-%m-%dT%H:%M:%S" format
    formatted_end_of_month = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    for item in training_data:
        try:
            generation_data = ESIOS.get_training_data(current_date, query_year, item)
            df = ESIOS.extract_values(generation_data, item)

            ESIOS.connection_to_DB(df, item, query_year)
        except Exception as e:
            print(f'Values were not found for {item} for the month{formatted_end_of_month}')
            print(e)

    current_date = current_date + relativedelta(years = 1)


# load data from MIBGAS since 2019
    
years = [2019, 2020, 2021, 2022, 2023]

for year in years:
    gas_data = mibgas.get_data(year)
    gas_data_cleaned = mibgas.adapt_data(gas_data)
    mibgas.connection_to_DB(gas_data_cleaned, year)