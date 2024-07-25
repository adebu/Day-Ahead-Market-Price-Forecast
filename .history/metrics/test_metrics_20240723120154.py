import os
import sys
from metrics import rmse, sMAPE
import pandas as pd
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
process_data_dir = os.path.abspath(os.path.join(parent_dir, 'process_data'))
models_data_dir = os.path.abspath(os.path.join(parent_dir, 'models'))
sys.path.insert(1, process_data_dir)
sys.path.insert(1, models_data_dir)
sys.path.insert(1, parent_dir)

from create_df import get_df
from classical_models import linear_regression, xgboost, adaboost, CART

X_train, X_test, y_train, y_test, test_dates= get_df()

print('Starting Calculations')
print('Linear Regression')
pred_regression = linear_regression(X_train, y_train, X_test)
reg_RMSE = rmse(pred_regression, y_test)
reg_sMAPE = sMAPE(pred_regression, y_test)

print('XGB')
pred_xgb = xgboost(X_train, y_train, X_test)
xgb_RMSE = rmse(pred_xgb, y_test)
xgb_sMAPE = sMAPE(pred_xgb, y_test)

print('ADABoost')
pred_ada = adaboost(X_train, y_train, X_test)
ada_RMSE = rmse(pred_ada, y_test)
ada_sMAPE = sMAPE(pred_ada, y_test)

print('CART')
pred_cart = CART(X_train, y_train, X_test)
cart_RMSE = rmse(pred_cart, y_test)
cart_sMAPE = sMAPE(pred_cart, y_test)


data = {
    'Model': ['Linear Regression', 'XGBoost', 'AdaBoost', 'CART'],
    'RMSE': [reg_RMSE, xgb_RMSE, ada_RMSE, cart_RMSE],
    'sMAPE': [reg_sMAPE, xgb_sMAPE, ada_sMAPE, cart_sMAPE]
    #'Model': ['Linear Regression', 'CART'],
    #'RMSE': [reg_RMSE,  cart_RMSE],
    #'sMAPE': [reg_sMAPE,  cart_sMAPE]
}

df_metrics = pd.DataFrame(data)
df_metrics.to_csv('classical_models_metrics.csv', index=False)

data_predictions = {
    'Date': test_dates['day'].to_numpy(),
    'hour': test_dates['hour'].to_numpy(),
    'Actual': y_test.to_numpy(),
    'Linear Regression': pred_regression,
    'XGBoost': pred_xgb,
    'AdaBoost': pred_ada,
    'CART': pred_cart
}
df_predictions = pd.DataFrame(data_predictions)

print(df_metrics)

# Optionally, save the DataFrame to a CSV file
df_metrics.to_csv('df_metrics.csv', index=False)



