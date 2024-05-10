import numpy as np

def rmse (y_pred, y_real):
    
    return np.sqrt(np.mean((y_real - y_pred)**2))


def sMAPE(y_pred, y_real):
    
    return np.mean(np.abs(y_real - y_pred) / ((np.abs(y_real) + np.abs(y_pred)) / 2))

def rMAE():
    pass
