import os

import pandas as pd

from config_file import data_path


def generate():
    path = os.path.join(data_path, "tracks.jsonl")
    df = pd.read_json(path, orient="records", lines=True)
    df_id = df[["id", "id_artist", "duration_ms"]]
    # save to csv
    df_id.to_csv(os.path.join(data_path, "track_artist_duration.csv"), index=False, header=True)


if __name__ == "__main__":
    generate()
