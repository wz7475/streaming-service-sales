import os

import pandas as pd

from config_file import data_path

if __name__ == "__main__":
    path = os.path.join(data_path, "artists.jsonl")
    df = pd.read_json(path, orient="records", lines=True)
    df_id = df[["id"]]
    # save to csv
    # include header
    df_id.to_csv(os.path.join(data_path, "artists_ids.csv"), index=False, header=True)