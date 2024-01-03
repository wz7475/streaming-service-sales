from math import sqrt
from sklearn.metrics import mean_squared_error
from config_file import data_path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import warnings
warnings.filterwarnings("ignore")
def prepare_df(artist_filename: str) -> pd.DataFrame:
    df = pd.read_csv(os.path.join(data_path, 'artists_sessions', artist_filename))
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df.drop(["id_artist"], axis=1, inplace=True)
    df["count"] = 1
    df_resampled = df.resample("M").sum()
    df_resampled.drop(df_resampled.tail(1).index, inplace=True)
    return df_resampled


def get_trained_model(train) -> SARIMAX:
    sarima = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    sarima_fit = sarima.fit(disp=False)
    return sarima_fit

def get_dummy_prediction(train, periods: int):
    dummy_pred = np.zeros(periods)
    for i in range(periods):
        if i == 0:
            dummy_pred[i] = train[- (periods) + i:].mean()
        else:
            dummy_pred[i] = train[- (periods) + i:].mean() * (periods - i) / periods + dummy_pred[:i].mean() * i / periods
    return dummy_pred


def check_artist(artist_id: str) -> (float, float):
    df_resampled = prepare_df(artist_id)
    train = df_resampled['count'].values[:len(df_resampled) - 8]
    test = df_resampled['count'].values[len(df_resampled) - 8:]
    sarima_fit = get_trained_model(train)
    pred = sarima_fit.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
    dummy_pred = get_dummy_prediction(train, len(test))

    sarima_rmse = sqrt(mean_squared_error(test, pred))
    dummy_rmse = sqrt(mean_squared_error(test, dummy_pred))
    sum_of_test = test.sum()
    return sarima_rmse / sum_of_test, dummy_rmse / sum_of_test


if __name__ == "__main__":
    all_artists = os.listdir(os.path.join(data_path, 'artists_sessions'))

    df_score = pd.DataFrame(columns=['artist_id', 'sarima_score', 'dummy_score'])
    for artist in all_artists:
        sarima_score, dummy_score = check_artist(artist)
        print(sarima_score, dummy_score)
        df_score = df_score._append({'artist_id': artist, 'sarima_score': sarima_score, 'dummy_score': dummy_score}, ignore_index=True)
    df_score.to_csv(os.path.join(data_path, 'sarima_dummy_scores.csv'), index=False)