from math import sqrt
from sklearn.metrics import mean_squared_error
from model.config_file import data_path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import warnings

warnings.filterwarnings("ignore")


def prepare_df(artist_filename: str) -> pd.DataFrame:
    df = pd.read_csv(
        os.path.join(data_path, 'artists_sessions', artist_filename))
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df.drop(["id_artist"], axis=1, inplace=True)
    df["count"] = 1
    df_resampled = df.resample("M").sum()
    df_resampled.drop(df_resampled.tail(1).index, inplace=True)
    return df_resampled


def avg_timeplay_artist(artist_id: str) -> float:
    df = pd.read_csv(os.path.join(data_path, "artists_duration.csv"))
    return df[df['id_artist'] == artist_id]["song_duration"].values[0]

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
            dummy_pred[i] = train[- (periods) + i:].mean() * (
                    periods - i) / periods + dummy_pred[
                                             :i].mean() * i / periods
    return dummy_pred


def check_artist(artist_id: str) -> (float, float):
    df_resampled = prepare_df(artist_id)
    train = df_resampled['count'].values[:len(df_resampled) - 8]
    test = df_resampled['count'].values[len(df_resampled) - 8:]
    sarima_fit = get_trained_model(train)
    pred = sarima_fit.predict(start=len(train), end=len(train) + len(test) - 1,
                              dynamic=False)
    dummy_pred = get_dummy_prediction(train, len(test))

    sarima_rmse = sqrt(mean_squared_error(test, pred))
    dummy_rmse = sqrt(mean_squared_error(test, dummy_pred))
    sum_of_test = test.sum()
    return sarima_rmse / sum_of_test, dummy_rmse / sum_of_test


class NaiveModel:
    def __init__(self, train, avg_timeplay: float):
        self.train = [t for t in train]
        self.avg_timeplay = avg_timeplay

    def predict(self, start, end: int, **kwargs):
        copy = [t for t in self.train]

        for period in range(len(self.train), max(len(self.train), end)):
            copy.append(
                sum(copy[-4 + period:]) / 4
            )

        return [c * self.avg_timeplay for c in copy[start:end]]


class ComplexModel:
    def __init__(self, model, avg_timeplay: float):
        self.model = model
        self.avg_timeplay = avg_timeplay

    def predict(self, start, end: int, **kwargs):
        return [c * self.avg_timeplay for c in self.model.predict(start, end)]


def get_naive_model(train, avg_timeplay):
    return NaiveModel(train, avg_timeplay)


def get_complex_model(train, avg_timeplay):
    return ComplexModel(get_trained_model(train), avg_timeplay)


def generate_model(artist_id: str, avg_timeplay):
    df_resampled = prepare_df(artist_id)
    sarima_fit = get_complex_model(df_resampled['count'].values, avg_timeplay)
    naive_fit = get_naive_model(df_resampled['count'].values, avg_timeplay)

    return naive_fit, sarima_fit


def generate_models():
    all_artists = os.listdir(
        os.path.join(os.getcwd(), data_path, "artists_sessions"))

    for i, artist in enumerate(all_artists):
        print(f'[{i} / {len(all_artists)}]{artist}')
        real_id = artist.replace('.csv', '')
        print(avg_timeplay_artist(real_id))
        naive, complex = generate_model(artist, avg_timeplay_artist(real_id))
        yield real_id, naive, complex


if __name__ == "__main__":
    all_artists = os.listdir(os.path.join(data_path, 'artists_sessions'))

    df_score = pd.DataFrame(
        columns=['artist_id', 'sarima_score', 'dummy_score'])
    for i, artist in enumerate(all_artists):
        print(f'[{i} / {len(all_artists)}]{artist}')
        sarima_score, dummy_score = check_artist(artist)
        print(sarima_score, dummy_score)
        df_score = df_score._append(
            {'artist_id': artist, 'sarima_score': sarima_score,
             'dummy_score': dummy_score}, ignore_index=True)
    df_score.to_csv(os.path.join(data_path, 'sarima_dummy_scores.csv'),
                    index=False)
