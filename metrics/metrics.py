import numpy as np
import pandas as pd
import os

def rmse (y_pred, y_real):
    
    return np.sqrt(np.mean((y_real - y_pred)**2))


def sMAPE(y_pred, y_real):
    
    return np.mean(np.abs(y_real - y_pred) / ((np.abs(y_real) + np.abs(y_pred)) / 2))

def rMAE():
    pass

def MAE(y_pred, y_real):
    return np.mean(np.abs(y_real - y_pred))


def calculate_metrics(y_pred, y_real, model_name):
    value_rmse = rmse (y_pred, y_real)
    value_sMAPE = sMAPE(y_pred, y_real)
    value_MAE = MAE(y_pred, y_real)

    data = {
    'Model': [model_name],
    'RMSE': [value_rmse],
    'sMAPE': [value_sMAPE],
    'MAE': [value_MAE]
}
    
    df_new = pd.DataFrame(data)

    # File path for the results
    file_path = 'Results.xlsx'
    
    print('Saving results to file...')
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, append the results
        df_existing = pd.read_excel(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(file_path, index=False)
    else:
        # If it doesn't exist, create a new file with the results
        df_new.to_excel(file_path, index=False)

    return df_new


