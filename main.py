from downloadFiles import get_training_data, extract_values, connection_to_DB
from datetime import datetime, timedelta

start_date = "2023-01-01T00:00:00"
end_date = "2023-10-01T00:00:00"

training_data = ['demand', 'wind', 'solar', 'spot_price']
historic_data = ['demand_historic', 'wind_historic', 'solar_historic', 'spot_historic']

# Convert start_date and end_date to datetime objects
start_date = datetime.fromisoformat(start_date)
end_date = datetime.fromisoformat(end_date)

while start_date <= end_date:
    # Calculate the end of the current month
    next_month = start_date.replace(day=1, hour=0, minute=0, second=0) + timedelta(days=32)
    end_of_month = (next_month - timedelta(days=next_month.day)).replace(hour=23, minute=59, second=59)

    # Format end_of_month in the "%Y-%m-%dT%H:%M:%S" format
    formatted_end_of_month = end_of_month.strftime("%Y-%m-%dT%H:%M:%S")
    for item in training_data:
        try:
            generation_data = get_training_data(start_date, end_date, item)
            df = extract_values(generation_data, item)
            #df.to_csv(f'{item}.csv')
            connection_to_DB(df, item)
        except:
            print(f'Values were not found for {item} for the month{formatted_end_of_month}')

    start_date = end_of_month + timedelta(seconds=1)



#Load marginalpdbf files into db
#test_df = df_to_db(dates)