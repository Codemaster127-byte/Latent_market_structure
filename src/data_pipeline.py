import numpy as np
import pandas as pd
import datetime
import time
import os
import glob
from functools import reduce


def map_data():
    df1 = pd.read_pickle("data/50_comp_df.pkl")
    return df1


def fetch_with_retry(kite, token, from_date, to_date, symbol, max_retries=3):
    for attempt in range(max_retries):
        try:
            return kite.historical_data(
                instrument_token=token,
                from_date=from_date,
                to_date=to_date,
                interval="day"
            )
        except Exception as e:
            print(f"{symbol} attempt {attempt+1} failed: {e}")
            time.sleep(1.5 * (attempt + 1))

    print(f"{symbol} completely failed.")
    return None


def get_2_year_data(df1, kite):
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=365 * 2)

    os.makedirs("data/cache", exist_ok=True)

    for _, row in df1.iterrows():
        token = row["id"]
        symbol = row["symbol"]

        file_path = f"data/cache/{symbol}.parquet"

        # skip if already fetched
        if os.path.exists(file_path):
            print(f"{symbol} already exists, skipping")
            continue

        data = fetch_with_retry(kite, token, from_date, to_date, symbol)

        if data is None:
            continue

        temp = pd.DataFrame(data)[["date", "close"]]
        temp = temp.rename(columns={"close": symbol})

        # save immediately (critical)
        temp.to_parquet(file_path)

        time.sleep(0.5)  # safer rate limit

    print("Data fetching complete.")


def merger_Via_Date():
    files = glob.glob("data/cache/*.parquet")

    if not files:
        print("No data files found.")
        return None

    frames = [pd.read_parquet(f) for f in files]

    final_df = reduce(
        lambda left, right: pd.merge(left, right, on="date", how="outer"),
        frames
    )

    final_df = final_df.sort_values("date").reset_index(drop=True)

    # handle missing values (important)
    final_df = final_df.fillna(method="ffill")

    print(final_df)

    return final_df