import os
import pandas as pd
from config_file import data_path


def generate_timestamp_artist():
    df_sessions = pd.read_csv(os.path.join(data_path, 'sessions_timestamp_track.csv'))

    df_tracks = pd.read_csv(os.path.join(data_path, 'tracks_ids.csv'))

    df_tracks.rename(columns={'id': 'track_id'}, inplace=True)

    df_session_artist = df_sessions.merge(df_tracks, on='track_id')
    df_session_artist = df_session_artist[['timestamp', 'id_artist']]

    df_session_artist.to_csv(os.path.join(data_path, 'timestamp_artist.csv'), index=False)

if __name__ == "__main__":
    generate_timestamp_artist()