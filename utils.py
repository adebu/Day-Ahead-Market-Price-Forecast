import pandas as pd

def adjust_timestamp(df):
    
    # divide and transform to datetime
    df[['timestamp_str', 'offset_str']] = df['datetime'].str.split('+', expand=True)
    df['timestamp_str'] = pd.to_datetime(df['timestamp_str'])

    # Get offset
    df['hour_offset'] = df['offset_str'].astype(str).str[0:2]
    df['minute_offset'] = df['offset_str'].astype(str).str[3:5]

    # Convert hour and minute offsets to timedelta objects
    df['timezone_offset'] = pd.to_timedelta(df['hour_offset'].astype(int), unit='h') + pd.to_timedelta(df['minute_offset'].astype(int), unit='m')
    df['datetime'] = df['timestamp_str'] + df['timezone_offset']
    df['datetime'] =df['datetime'].astype(str)

    return df