create_values_df = '''
SELECT * 
FROM gas_data, wind, solar, demand, spot_price
JOIN demand ON demand.day = gas_data.delivery_day 
'''