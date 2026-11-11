
from pathlib import Path

import numpy as np
import pandas as pd


def generate_gps_data(number_of_records=10_000, seed=42):
    """
    Generate simulated, anonymized GPS pings around Bhopal.

    This dataset is synthetic and does not represent real people.
    """

    rng = np.random.default_rng(seed)

    # Approximate central coordinates of Bhopal
    center_latitude = 23.2599
    center_longitude = 77.4126

    # Generate locations within an approximate study area
    latitudes = rng.normal(center_latitude, 0.035, number_of_records)
    longitudes = rng.normal(center_longitude, 0.035, number_of_records)

    # Generate anonymous device identifiers
    device_ids = [
        f"DEVICE_{number:06d}"
        for number in rng.integers(1, 2001, number_of_records)
    ]

    # Generate timestamps across a simulated 7-day period
    start_time = pd.Timestamp("2026-01-01 00:00:00")

    random_seconds = rng.integers(
        0,
        7 * 24 * 60 * 60,
        number_of_records
    )

    timestamps = start_time + pd.to_timedelta(
        random_seconds, unit="s"
    )

    data = pd.DataFrame({
        "DeviceID": device_ids,
        "Lat": latitudes,
        "Long": longitudes,
        "Timestamp": timestamps
    })

    return data


def save_gps_data(data):
    """Save generated GPS data to the raw data folder."""

    output_path = Path("data/raw/gps_pings.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(output_path, index=False)

    print(f"Dataset saved to: {output_path}")
    print(f"Total GPS records: {len(data):,}")


if __name__ == "__main__":
    gps_data = generate_gps_data()
    save_gps_data(gps_data)

    print("\nFirst five records:")
    print(gps_data.head())
