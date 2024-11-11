
from pmdarima import auto_arima
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
import warnings

def model_auto_arima(df_3719_week, forecast_steps):
    with warnings.catch_warnings():
        # Filter only ValueWarning and FutureWarning messages related to index
        warnings.filterwarnings("ignore", message="No supported index is available", category=UserWarning)
        warnings.filterwarnings("ignore", message="No supported index is available", category=FutureWarning)
        
        # Since I don't have time for hyperparameter tuning, I'll try with auto_arima
        model = auto_arima(df_3719_week['quantity1'], 
                           seasonal=False,  # no seasonal pattern
                           trace=True,         
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)   
            
        # Fit the model
        model.fit(df_3719_week['quantity1'])
            
        # Forecast the next few time periods (e.g., 5 steps forward)
        forecast = model.predict(n_periods=forecast_steps)
            
        # Display the forecast
        print("Forecast for the next periods:")
        print(forecast)
            
        # Calculate RMSE on the in-sample data (just to check the initial model fit)
        in_sample_forecast = model.predict_in_sample()
        rmse_in_sample = np.sqrt(mean_squared_error(df_3719_week['quantity1'], in_sample_forecast))
        print(f'In-sample RMSE: {rmse_in_sample:.2f}')
        print(model.summary())
        return forecast

def model_auto_arima_cross(df_3719_week, forecast_steps, splitting):
    # Ensure 'delivery_date' is a datetime index (remove if already confirmed)
    df_3719_week.index = pd.DatetimeIndex(df_3719_week.index)
    
    # Initialize TimeSeriesSplit for cross-validation
    tscv = TimeSeriesSplit(n_splits=splitting)
    
    # Store RMSE scores for each fold
    rmse_scores = []
    
    # Cross-validation loop
    for train_index, test_index in tscv.split(df_3719_week):
        # Split the data into train and test sets for the current fold
        train, test = df_3719_week.iloc[train_index], df_3719_week.iloc[test_index]
        
        # Fit auto_arima on the training set
        model = auto_arima(train['quantity1'], 
                           seasonal=False, 
                           trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
        
        # Forecast for the length of the test set
        forecast = model.predict(n_periods=len(test))
        # Display the forecast
        print("Forecast for the next periods:")
        print(forecast)
        
        # Calculate RMSE for the current fold
        rmse = np.sqrt(mean_squared_error(test['quantity1'], forecast))
        rmse_scores.append(rmse)
        print(f'Fold RMSE: {rmse:.2f}')
    
    # Calculate the average RMSE across all folds
    average_rmse = np.mean(rmse_scores)
    print(f'Average RMSE across all folds: {average_rmse:.2f}')
    

