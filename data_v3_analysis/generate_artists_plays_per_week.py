import os
import pandas as pd
from config_file import data_path

# mute warnings
import warnings
warnings.filterwarnings('ignore')

def _get_sessions_per_week(artist_id: str, df: pd.DataFrame) -> pd.DataFrame:
    df_artist = df[df['id_artist'] == artist_id]
    df_artist['week'] = df_artist['timestamp'].dt.dayofyear // 7
    df_artist["week"] = df_artist["week"].astype(str).str.zfill(2)
    df_artist['year'] = df_artist['timestamp'].dt.year
    df_artist['year'] = df_artist['year'].astype(str)
    df_artist['year_week'] = df_artist['year'] + '_' + df_artist['week']
    df_artist = df_artist[['year_week', 'id_artist']]
    df_artist = df_artist.groupby('year_week').count()
    # sort by year_week desc
    df_artist.sort_index(ascending=False, inplace=True)
    # reverse index
    df_artist = df_artist.iloc[::-1]
    df_artist.rename(columns={'id_artist': 'count'}, inplace=True)
    return df_artist


def generate_artists_plays_per_week():
    df_session_artist = pd.read_csv(os.path.join(data_path, 'timestamp_artist.csv'))
    df_session_artist['timestamp'] = pd.to_datetime(df_session_artist['timestamp'])

    all_artists = df_session_artist['id_artist'].unique()
    plays_per_week = [_get_sessions_per_week(artist_id, df_session_artist) for artist_id in all_artists]

    # save to file plays per week
    os.makedirs(os.path.join(data_path, 'plays_per_week'), exist_ok=True)
    print("started saving plays per week")
    counter = 1
    for artist_weeks, artist_id in zip(plays_per_week, all_artists):
        artist_weeks.to_csv(os.path.join(data_path, 'plays_per_week', artist_id + '.csv'))
        print(f"saved plays per week for artist: {counter}/{len(all_artists)}")
        counter += 1

    print("finished saving plays per week")


if __name__ == "__main__":
    generate_artists_plays_per_week()
