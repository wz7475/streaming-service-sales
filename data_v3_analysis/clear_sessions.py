import os

import pandas as pd

from config_file import data_path


def clear_sessions():
    path = os.path.join(data_path, "sessions.jsonl")
    if os.path.exists(os.path.join(data_path, "sessions_timestamp_track.csv")):
        os.remove(os.path.join(data_path, "sessions_timestamp_track.csv"))
    for chunk in pd.read_json(path, orient="records", lines=True, chunksize=1000000):
        print(type(chunk))
        chunk_play = chunk[chunk["event_type"] == "play"]
        chunk_play = chunk_play[["timestamp", "track_id"]]
        # save to csv
        chunk_play.to_csv(os.path.join(data_path, "sessions_timestamp_track.csv"), index=False, mode="a", header=True)


if __name__ == "__main__":
    clear_sessions()
