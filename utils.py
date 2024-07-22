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

def get_appendix(inputs):
    
    if inputs == 'spot_price':
        appendix = '&geo_ids[]=3'
    elif inputs == 'nuclear':
        appendix = '&geo_agg=sum&time_trunc=hour'
    else:
        appendix = ''
    
    return appendix

def adjust_date(*args):
    from datetime import datetime, timedelta

    if len(args) == 2:
        day = args[0]
        hour = args[1]
        adjusted_datetime = datetime.strptime(f"{day} {hour}", "%Y-%m-%d %H:%M") + timedelta(hours=1)
        return adjusted_datetime.strftime("%Y-%m-%d %H:%M:%S")
    elif len(args) == 1:
        day = args[0]
        adjusted_datetime = datetime.strptime(f"{day}", "%Y-%m-%d") + timedelta(days=1)
        return adjusted_datetime.strftime("%Y-%m-%d")

    else:
        raise ValueError("Issue encountered when updating dataset. Date-hour format not valid")


