import sqlite3

def check_table_existence():
    try:
        conn = sqlite3.connect('Main_DB')
        c = conn.cursor()

        # Check if the table 'gas_data' exists
        c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='gas_data'")
        result = c.fetchone()

        if result:
            print("Table 'gas_data' exists")
        else:
            print("Table 'gas_data' does not exist")

        conn.close()

    except Exception as e:
        print('Error checking table existence:', e)

# Call the function to check if the table exists
check_table_existence()
