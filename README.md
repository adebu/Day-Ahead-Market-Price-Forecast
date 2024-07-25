# Day Ahead Market Price Forecast

## How does the Day Ahead Market Work

The Day-Ahead Electricity Market in Europe plays a crucial role in the overall functioning of the electricity market by enabling power trading for the upcoming day. This market operates through a structured process that ensures efficiency, transparency, and the optimal allocation of electricity across various regions.

A more in depth of how electricity markets work and integrate together can be found in the videos prepared by the Florence School of Regulation: [Video Lectures](https://www.youtube.com/watch?v=U6d0X-TabQk)

Forecasting electricity market prices in Europe is crucial for both consumers and producers. For consumers, accurate forecasts allow better budget planning and informed decisions about energy use, potentially lowering costs. Producers benefit by optimizing generation schedules and maximizing revenues, making strategic decisions about when to adjust production. Accurate forecasts are also essential for integrating renewable energy sources into the grid, ensuring stability and reliability.

## Features

###  Models

* **Linear Regression:** Used default hyperparameters without tuning.
* **Decision Tree (CART):** Set ```random_state``` and ```min_samples_split```, others are default.
* **XGBoost:** Grid search was used to tune hyperparameters (```n_estimators, learning_rate, max_depth, subsample, colsample_bytree```).
* **AdaBoost:** Random search was used to tune hyperparameters (```n_estimators, learning_rate, loss```).

---
* **DNN** Optuna was used to optimize the folowing hyperparameters: ```scaler, n_layers, n_neurons, epochs, batch_size```

### Data

* REE's forecast: D+1 Hourly forecast of Wind, Solar and Nuclear generation (resolution = hourly)
* D-1 Energy Market hourly price (resolution = hourly)
* Gas Price: Day ahead price provided by MIBGAS (resolution = daily)

### Metrics
Standard evaluation metrics commonly used in the literature were selected; MAE, sMAPE and RMSE [[1]](#1)



## Results
| Model | RMSE | sMAPE | 
| --- | --- | --- | 
| Linear Regression | 25.68 | 0.249 | 
| CART | 14.42 | 0.153 |
| XGBoost | 26.45 | 0.273 |
| ADABoost | 18.92 | 0.166 |
| DNN | 13.96 | 0.134 |
  
## Next Steps
* Feature Selection: feature selection is a common practice in both deep learning and forecasting energy market prices [[1]](#1) and can help to improve the accuracy of the models.
* Hyperparameter Tuning: In this version, single-step forecasting is used. That means that the neural network predicts the electricity price for the next hour based on the input data. However, some authors found better results when applying multi-step forecasting, where the neural network predicts electricity prices for the next 24 hours simultaneously [[1]](#1)
* Data Granularity and new features: Some relevant factors like the natural gas price are very relevant to determining the marginal price. However, this data is usually given daily. Other features such as temperature in major cities have been succesfully used [[2]](#2)
* Check accuracy of REE's Forecast:  Our model's data is very dependent on the accuracy of REE's solar, wind, nuclear, and demand forecast. Small errors can compound and significantly impact the reliability of our predictions. It is crucial to evaluate the forecast's accuracy and consider potential improvements or adjustments to ensure that our model's performance is not adversely affected by forecast inaccuracies.
* Use different methods proposed in different papers like LSTM [[3]](#3), ensemble methods [[4]](#4) or CNN [[5]](#5)
* Improve metrics: include standard statistical tests such as Diebold-Mariano to evaluate statistical differences [[1]](#1).

The final objective of this project is to provide a reliable forecast of the Day Ahead Energy Market price for several regions of Europe.

## References
<a id="1">[1]</a> 
Jesus Lago, Grzegorz Marcjasz, Bart De Schutter, Rafał Weron,
Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark,
Applied Energy,
Volume 293,
2021,
116983,
ISSN 0306-2619,
https://doi.org/10.1016/j.apenergy.2021.116983.

<a id="2">[2]</a>
https://www.kaggle.com/code/dimitriosroussis/electricity-price-forecasting-with-dnns-eda

<a id="3">[3]</a> 
S. Zhou, L. Zhou, M. Mao, H. -M. Tai and Y. Wan, "An Optimized Heterogeneous Structure LSTM Network for Electricity Price Forecasting," in IEEE Access, vol. 7, pp. 108161-108173, 2019



<a id="4">[4]</a>
Michał Narajewski, Florian Ziel,
Ensemble forecasting for intraday electricity prices: Simulating trajectories,
Applied Energy,
Volume 279,
2020,
115801,
ISSN 0306-2619,
https://doi.org/10.1016/j.apenergy.2020.115801.

<a id="5">[5]</a> 
Ahmad W, Javaid N, Chand A, Shah SYR, Yasin U, Khan M, et al. Electricity
price forecasting in smart grid: A novel E-CNN model. In: Web, Artificial
Intelligence and Network Applications. Springer International Publishing; 2019,
p. 1132–44. http://dx.doi.org/10.1007/978-3-030-15035-8_109.

