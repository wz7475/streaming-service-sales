import os

import pandas as pd

from config_file import data_path


def generate():
    path = os.path.join(data_path, "sessions.jsonl")
    if os.path.exists(os.path.join(data_path, "timestamp_track_event_type.csv")):
        os.remove(os.path.join(data_path, "timestamp_track_event_type.csv"))
    for chunk in pd.read_json(path, orient="records", lines=True, chunksize=1000000):
        print(type(chunk))
        chunk.drop(["session_id", "user_id"], axis=1, inplace=True)

        # save to csv
        chunk.to_csv(os.path.join(data_path, "timestamp_track_event_type.csv"), index=True, mode="a", header=True)


if __name__ == "__main__":
    generate()
