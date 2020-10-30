import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
import streamlit as st


def app():
    st.title('Data Decomposition and Forecasting')
    st.subheader('Daily Confirmed with Mean')

    # Extract Data while setting Date as index and replacing NaN values
    df = pd.read_csv('Covid-19 SG for data decomp.csv')
    df["Date"] = pd.to_datetime(df["Date"], format='%d/%m/%Y')
    df = df.replace(np.NaN, 0)
    df = df.set_index('Date')

    # Produce Mean graph of Daily Confirmed Cases
    y = df['Daily_Confirmed']
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.plot(y, marker='.', linestyle='-', linewidth=0.5, label='Weekly')
    ax.plot(y.resample('M').mean(), marker='o', markersize=8, linestyle='-', label='Monthly Mean Resample')
    ax.set_ylabel('Daily_Confirmed')
    ax.legend();
    st.pyplot(fig)

    # Decomposing Data to view characteristics like seasonal trend and General Trend
    def seasonal_decompose(y):
        decomposition = sm.tsa.seasonal_decompose(y, model='additive', extrapolate_trend='freq')
        fig = decomposition.plot()
        fig.set_size_inches(14, 7)
        st.pyplot(fig)

    st.subheader('Decomposed Data')

    seasonal_decompose(y)

    ### plot for Rolling Statistic for testing Stationarity
    def test_stationarity(timeseries, title):
        # Determing rolling statistics
        rolmean = pd.Series(timeseries).rolling(window=12).mean()
        rolstd = pd.Series(timeseries).rolling(window=12).std()

        fig, ax = plt.subplots(figsize=(16, 4))
        ax.plot(timeseries, label=title)
        ax.plot(rolmean, label='rolling mean');
        ax.plot(rolstd, label='rolling std (x10)');
        ax.legend()
        st.pyplot(fig)

    pd.options.display.float_format = '{:.8f}'.format
    st.subheader('Raw Data Augmented Dickey-Fuller Test')

    test_stationarity(y, 'raw data')

    # Augmented Dickey-Fuller Test

    def ADF_test(timeseries, dataDesc):
        st.write('Is the {} stationary ?'.format(dataDesc))
        dftest = adfuller(timeseries.dropna(), autolag='AIC')
        st.write('Test statistic = {:.3f}'.format(dftest[0]))
        st.write('P-value = {:.3f}'.format(dftest[1]))
        st.write('Critical values :')
        for k, v in dftest[4].items():
            st.write(
                '\t{}: {} - The data is {} stationary with {}% confidence'.format(k, v, 'not' if v < dftest[0] else '',
                                                                                  100 - int(k[:-1])))

    ADF_test(y, 'raw data')

    y_detrend = (y - y.rolling(window=12).mean()) / y.rolling(window=12).std()

    st.subheader('De-trended Data Augmented Dickey-Fuller Test')

    test_stationarity(y_detrend, 'de-trended data')
    ADF_test(y_detrend, 'de-trended data')

    # Differencing
    y_12lag = y - y.shift(12)

    st.subheader('Differenced Augmented Dickey-Fuller Test')

    test_stationarity(y_12lag, '12 lag differenced data')
    ADF_test(y_12lag, '12 lag differenced data')

    # Detrending + Differencing

    y_12lag_detrend = y_detrend - y_detrend.shift(12)

    st.subheader('Differenced and De-trended Augmented Dickey-Fuller Test')

    test_stationarity(y_12lag_detrend, '12 lag differenced de-trended data')
    ADF_test(y_12lag_detrend, '12 lag differenced de-trended data')

    y_to_train = y[:'2020-07-31']  # dataset to train
    y_to_val = y['2020-07-31':]  # last X months for test
    predict_date = len(y) - len(y[:'2020-07-31'])  # the number of data points for the test set

    st.subheader('Forecasting Using Holt-Winters Exponential Smoothing')

    st.set_option('deprecation.showPyplotGlobalUse', False)

    def holt_win_sea(y, y_to_train, y_to_test, seasonal_type, seasonal_period, predict_date):
        y.plot(marker='o', color='black', legend=True, figsize=(14, 7))

        if seasonal_type == 'additive':
            fit1 = ExponentialSmoothing(y_to_train, seasonal_periods=seasonal_period, trend='add', seasonal='add').fit(
                use_boxcox=True)
            fcast1 = fit1.forecast(steps=200).rename('Additive')
            mse1 = ((fcast1 - y_to_test) ** 2).mean()
            st.write('The Root Mean Squared Error of additive trend, additive seasonal of ' +
                     'period season_length={} and a Box-Cox transformation {}'.format(seasonal_period,
                                                                                      round(np.sqrt(mse1), 2)))

            fit2 = ExponentialSmoothing(y_to_train, seasonal_periods=seasonal_period, trend='add', seasonal='add',
                                        damped_trend=True).fit(use_boxcox=True)
            fcast2 = fit2.forecast(steps=200).rename('Additive+damped')
            mse2 = ((fcast2 - y_to_test) ** 2).mean()
            st.write('The Root Mean Squared Error of additive damped trend, additive seasonal of ' +
                     'period season_length={} and a Box-Cox transformation {}'.format(seasonal_period,
                                                                                      round(np.sqrt(mse2), 2)))

            fit1.fittedvalues.plot(style='--', color='red')
            fcast1.plot(style='--', marker='o', color='red', legend=True)
            fit2.fittedvalues.plot(style='--', color='green')
            fcast2.plot(style='--', marker='o', color='green', legend=True)

        elif seasonal_type == 'multiplicative':
            fit3 = ExponentialSmoothing(y_to_train, seasonal_periods=seasonal_period, trend='add', seasonal='mul').fit(
                use_boxcox=True)
            fcast3 = fit3.forecast(predict_date).rename('Multiplicative')
            mse3 = ((fcast3 - y_to_test) ** 2).mean()
            st.write('The Root Mean! Squared Error of additive trend, multiplicative seasonal of ' +
                     'period season_length={} and a Box-Cox transformation {}'.format(seasonal_period,
                                                                                      round(np.sqrt(mse3), 2)))

            fit4 = ExponentialSmoothing(y_to_train, seasonal_periods=seasonal_period, trend='add', seasonal='mul',
                                        damped=True).fit(use_boxcox=True)
            fcast4 = fit4.forecast(predict_date).rename('Multiplicative+damped')
            mse4 = ((fcast3 - y_to_test) ** 2).mean()
            st.write('The Root Mean! Squared Error of additive damped trend, multiplicative seasonal of ' +
                     'period season_length={} and a Box-Cox transformation {}'.format(seasonal_period,
                                                                                      round(np.sqrt(mse4), 2)))

            fit3.fittedvalues.plot(style='--', color='red')
            fcast3.plot(style='--', marker='o', color='red', legend=True)
            fit4.fittedvalues.plot(style='--', color='green')
            fcast4.plot(style='--', marker='o', color='green', legend=True)

        else:
            st.write('Wrong Seasonal Type. Please choose between additive and multiplicative')
        st.pyplot()

    holt_win_sea(y, y_to_train, y_to_val, 'additive', 52, predict_date)
