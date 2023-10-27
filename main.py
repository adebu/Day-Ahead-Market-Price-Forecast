from downloadFiles import get_generation_data, extract_values

#Inputs (example)
start_date = "2023-10-01T00:00:00"
end_date = "2023-10-02T00:00:00"
call_data = "hydro"
generation_data = get_generation_data(start_date, end_date, call_data)


dataframe = extract_values(generation_data, call_data)

print(dataframe)


#Load marginalpdbf files into db
#test_df = df_to_db(dates)