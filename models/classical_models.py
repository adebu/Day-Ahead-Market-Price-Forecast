from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_regression
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform



def xgboost(X_train, y_train, X_test):
    # Generate synthetic regression data
    X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

    # Define XGBoost regressor
    reg = xgb.XGBRegressor()

    # Define the hyperparameter grid to search
    param_grid = {
        'n_estimators': [100, 500, 1000],  
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }

    # Perform Grid Search with cross-validation
    grid_search = GridSearchCV(estimator=reg, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X, y)

    # Get the best parameters and best estimator
    best_params = grid_search.best_params_
    best_estimator = grid_search.best_estimator_


    reg_best_parameters = xgb.XGBRegressor(colsample_bytree = best_params['colsample_bytree'],\
                                       learning_rate = best_params['learning_rate'],\
                                       max_depth = best_params['max_depth'],\
                                       n_estimators = best_params['n_estimators'],\
                                       subsample = best_params['subsample'])
    
    xg_model = reg_best_parameters.fit(X_train, y_train)

    pred_xgboost = xg_model.predict(X_test)

    return pred_xgboost

def linear_regression(X_train, y_train, X_test):
    reg = LinearRegression().fit(X_train, y_train)
    pred_reg = reg.predict(X_test)

    return pred_reg

def adaboost(X_train, y_train, X_test):
    # Generate synthetic regression data
    X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

    # Define AdaBoost regressor with DecisionTreeRegressor as the base estimator
    reg = AdaBoostRegressor(base_estimator=DecisionTreeRegressor())

    # Define the hyperparameter distributions to search
    param_dist = {
        'n_estimators': [50, 100, 200, 300],  
        'learning_rate': uniform(0.01, 0.2 - 0.01),  
        'loss': ['linear', 'square', 'exponential'],  
        'base_estimator__max_depth': [1, 2, 3],  # Decision tree depth
        'base_estimator__min_samples_split': [2, 5, 10],  # Minimum samples required to split
        'base_estimator__min_samples_leaf': [1, 2, 4],  # Minimum samples required at each leaf node
    }

    # Perform Randomized Search with cross-validation
    random_search = RandomizedSearchCV(estimator=reg, param_distributions=param_dist, n_iter=20, cv=5, scoring='neg_mean_squared_error', random_state=42)
    random_search.fit(X_train, y_train)

    # Get the best parameters and best estimator
    best_params = random_search.best_params_
    best_estimator = random_search.best_estimator_

    pred_ADA = best_estimator.predict(X_test)

    return pred_ADA

def CART(X_train, y_train, X_test):
    regressor = DecisionTreeRegressor(random_state=42, min_samples_split=50)
    regressor.fit(X_train, y_train)

    # Predict on the test set
    pred_CART = regressor.predict(X_test)

    return pred_CART