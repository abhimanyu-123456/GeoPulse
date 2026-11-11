
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = ["DeviceID", "Lat", "Long", "Timestamp"]


def load_gps_data(file_path="data/raw/gps_pings.csv"):
    """Load GPS data and parse timestamps."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"GPS data not found: {path}")

    df = pd.read_csv(path)

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
    df["Long"] = pd.to_numeric(df["Long"], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLUMNS)

    df = df[
        df["Lat"].between(-90, 90)
        & df["Long"].between(-180, 180)
    ].copy()

    df = df.drop_duplicates()

    df = df.sort_values(
        ["DeviceID", "Timestamp"]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":
    gps_data = load_gps_data()

    print("GPS PREPROCESSING REPORT")
    print("=" * 35)
    print(f"Records after cleaning: {len(gps_data):,}")
    print(f"Unique devices: {gps_data['DeviceID'].nunique():,}")
    print(f"Date range: {gps_data['Timestamp'].min()} to "
          f"{gps_data['Timestamp'].max()}")
    print("\nSample records:")
    print(gps_data.head())
