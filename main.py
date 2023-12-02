from downloadFiles import get_training_data, extract_values, connection_to_DB
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ESIOS import ESIOS
from mibgas import mibgas

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

            connection_to_DB(df, item)
        except:
            print(f'Values were not found for {item} for the month{formatted_end_of_month}')

    current_date = current_date + relativedelta(years = 1)


# load gas data
years = [2019, 2020, 2021, 2022, 2023]

for year in years:
    gas_data = mibgas.get_data(year)
    gas_data_cleaned = mibgas.extract_data(gas_data)
    gas_data_cleaned.to_csv(f'gas_data_{year}.csv')