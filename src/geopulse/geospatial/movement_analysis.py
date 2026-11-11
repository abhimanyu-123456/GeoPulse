
from pathlib import Path

import pandas as pd
from geopy.distance import geodesic


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "gps_pings.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

MOVEMENT_OUTPUT = OUTPUT_DIR / "movement_metrics.csv"

SUMMARY_OUTPUT = OUTPUT_DIR / "device_movement_summary.csv"


# --------------------------------------------------
# LOAD GPS DATA
# --------------------------------------------------

def load_gps_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"GPS dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "DeviceID",
        "Lat",
        "Long",
        "Timestamp"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    if df["Timestamp"].isna().any():
        raise ValueError("Invalid timestamps found.")

    if df[["Lat", "Long"]].isna().any().any():
        raise ValueError("Missing GPS coordinates found.")

    df = df.sort_values(
        by=["DeviceID", "Timestamp"]
    ).reset_index(drop=True)

    return df


# --------------------------------------------------
# CALCULATE DISTANCE BETWEEN GPS OBSERVATIONS
# --------------------------------------------------

def calculate_distance(row):

    if pd.isna(row["Previous_Lat"]):
        return 0.0

    current_location = (
        row["Lat"],
        row["Long"]
    )

    previous_location = (
        row["Previous_Lat"],
        row["Previous_Long"]
    )

    distance = geodesic(
        previous_location,
        current_location
    ).kilometers

    return distance


# --------------------------------------------------
# PERFORM MOVEMENT ANALYSIS
# --------------------------------------------------

def perform_movement_analysis(df):

    df = df.copy()

    grouped = df.groupby("DeviceID")

    # Previous GPS coordinates for each device
    df["Previous_Lat"] = grouped["Lat"].shift(1)

    df["Previous_Long"] = grouped["Long"].shift(1)

    # Previous timestamp for each device
    df["Previous_Timestamp"] = grouped["Timestamp"].shift(1)

    # Time difference in seconds
    df["Time_Difference_Seconds"] = (
        df["Timestamp"] - df["Previous_Timestamp"]
    ).dt.total_seconds()

    # Distance between consecutive observations
    df["Distance_KM"] = df.apply(
        calculate_distance,
        axis=1
    )

    # Calculate speed in kilometres per hour
    elapsed_hours = (
        df["Time_Difference_Seconds"] / 3600
    )

    df["Speed_KMH"] = (
        df["Distance_KM"] / elapsed_hours
    )

    # First observation and zero-time intervals
    # do not have a meaningful speed.
    df.loc[
        df["Time_Difference_Seconds"].isna()
        | (df["Time_Difference_Seconds"] <= 0),
        "Speed_KMH"
    ] = float("nan")

    return df


# --------------------------------------------------
# CREATE DEVICE-WISE MOVEMENT SUMMARY
# --------------------------------------------------

def create_device_summary(df):

    summary = (
        df.groupby("DeviceID")
        .agg(
            Total_Observations=("DeviceID", "size"),
            Total_Distance_KM=("Distance_KM", "sum"),
            Average_Speed_KMH=("Speed_KMH", "mean"),
            Maximum_Speed_KMH=("Speed_KMH", "max")
        )
        .reset_index()
    )

    summary = summary.round(3)

    return summary


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\nGEO PULSE - MOVEMENT ANALYTICS")
    print("=" * 45)

    # Load GPS dataset
    df = load_gps_data()

    print(f"GPS records loaded: {len(df):,}")

    print(
        f"Unique devices: {df['DeviceID'].nunique():,}"
    )

    # Calculate movement metrics
    movement_df = perform_movement_analysis(df)

    # Create device-wise summary
    summary_df = create_device_summary(movement_df)

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save movement metrics
    movement_df.to_csv(
        MOVEMENT_OUTPUT,
        index=False
    )

    # Save device summary
    summary_df.to_csv(
        SUMMARY_OUTPUT,
        index=False
    )

    print("\nMOVEMENT ANALYSIS COMPLETED")
    print("-" * 45)

    print(
        f"Total movement records: {len(movement_df):,}"
    )

    print(
        f"Devices analyzed: {len(summary_df):,}"
    )

    print("\nDEVICE MOVEMENT SUMMARY")
    print(summary_df.head(10).to_string(index=False))

    print("\nOUTPUT FILES")
    print(f"1. {MOVEMENT_OUTPUT}")
    print(f"2. {SUMMARY_OUTPUT}")

    print("\nMovement analytics completed successfully!")


if __name__ == "__main__":
    main()
