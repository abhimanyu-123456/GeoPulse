
from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "movement_metrics.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

PATTERN_OUTPUT = OUTPUT_DIR / "movement_patterns.csv"

SUMMARY_OUTPUT = OUTPUT_DIR / "device_pattern_summary.csv"


# --------------------------------------------------
# LOAD MOVEMENT DATA
# --------------------------------------------------

def load_movement_data():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Movement dataset not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "DeviceID",
        "Timestamp",
        "Time_Difference_Seconds",
        "Distance_KM",
        "Speed_KMH"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    numeric_columns = [
        "Time_Difference_Seconds",
        "Distance_KM",
        "Speed_KMH"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# --------------------------------------------------
# CLASSIFY MOVEMENT SPEED
# --------------------------------------------------

def classify_speed(df):

    df = df.copy()

    valid_speeds = df["Speed_KMH"].dropna()

    if valid_speeds.empty:
        raise ValueError(
            "No valid speed observations available."
        )

    # Dataset-specific 99th percentile
    speed_threshold = valid_speeds.quantile(0.99)

    conditions = [
        df["Speed_KMH"].isna(),
        df["Speed_KMH"] > speed_threshold,
        df["Speed_KMH"] <= 0.5,
        df["Speed_KMH"].between(
            0.5,
            5,
            inclusive="right"
        ),
        df["Speed_KMH"] > 5
    ]

    categories = [
        "Insufficient Data",
        "Unusually High Speed",
        "Low Speed",
        "Moderate Speed",
        "Faster Movement"
    ]

    df["Speed_Category"] = np.select(
        conditions,
        categories,
        default="Unclassified"
    )

    return df, speed_threshold


# --------------------------------------------------
# IDENTIFY POTENTIAL STATIONARY OBSERVATIONS
# --------------------------------------------------

def identify_stationary_periods(df):

    df = df.copy()

    interval_minutes = (
        df["Time_Difference_Seconds"] / 60
    )

    conditions = [
        (
            df["Distance_KM"].notna()
            & df["Time_Difference_Seconds"].notna()
            & (df["Distance_KM"] <= 0.05)
            & (interval_minutes <= 30)
            & (interval_minutes > 0)
        )
    ]

    df["Potential_Stationary"] = np.select(
        conditions,
        [True],
        default=False
    )

    return df


# --------------------------------------------------
# CALCULATE MOVEMENT FREQUENCY
# --------------------------------------------------

def calculate_movement_frequency(df):

    frequency = (
        df.groupby("DeviceID")
        .agg(
            GPS_Observations=("DeviceID", "size"),
            First_Observation=("Timestamp", "min"),
            Last_Observation=("Timestamp", "max"),
            Average_Interval_Minutes=(
                "Time_Difference_Seconds",
                "mean"
            ),
            Median_Interval_Minutes=(
                "Time_Difference_Seconds",
                "median"
            )
        )
        .reset_index()
    )

    frequency[
        [
            "Average_Interval_Minutes",
            "Median_Interval_Minutes"
        ]
    ] = (
        frequency[
            [
                "Average_Interval_Minutes",
                "Median_Interval_Minutes"
            ]
        ] / 60
    )

    return frequency


# --------------------------------------------------
# CREATE DEVICE-WISE PATTERN SUMMARY
# --------------------------------------------------

def create_pattern_summary(df):

    summary = (
        df.groupby("DeviceID")
        .agg(
            Total_Observations=("DeviceID", "size"),
            Potential_Stationary_Count=(
                "Potential_Stationary",
                "sum"
            ),
            Low_Speed_Count=(
                "Speed_Category",
                lambda x: (x == "Low Speed").sum()
            ),
            Moderate_Speed_Count=(
                "Speed_Category",
                lambda x: (x == "Moderate Speed").sum()
            ),
            Faster_Movement_Count=(
                "Speed_Category",
                lambda x: (x == "Faster Movement").sum()
            ),
            High_Speed_Anomaly_Count=(
                "Speed_Category",
                lambda x: (
                    x == "Unusually High Speed"
                ).sum()
            )
        )
        .reset_index()
    )

    frequency = calculate_movement_frequency(df)

    summary = summary.merge(
        frequency,
        on="DeviceID",
        how="left"
    )

    return summary.round(3)


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\nGEO PULSE - MOVEMENT PATTERN ANALYSIS")
    print("=" * 50)

    # Load data
    df = load_movement_data()

    print(f"Records loaded: {len(df):,}")

    print(
        f"Devices analyzed: {df['DeviceID'].nunique():,}"
    )

    # Classify movement speeds
    df, threshold = classify_speed(df)

    print(
        f"\n99th percentile speed threshold: "
        f"{threshold:.3f} km/h"
    )

    # Identify potential stationary observations
    df = identify_stationary_periods(df)

    # Create device-wise summary
    summary = create_pattern_summary(df)

    # Save output files
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PATTERN_OUTPUT,
        index=False
    )

    summary.to_csv(
        SUMMARY_OUTPUT,
        index=False
    )

    # Display category counts
    print("\nSPEED CATEGORY DISTRIBUTION")
    print("-" * 40)

    print(
        df["Speed_Category"]
        .value_counts()
        .to_string()
    )

    print("\nPOTENTIAL STATIONARY OBSERVATIONS")

    print(
        int(df["Potential_Stationary"].sum())
    )

    print("\nDEVICE PATTERN SUMMARY")

    print(
        summary.head(10).to_string(index=False)
    )

    print("\nOUTPUT FILES")
    print(f"1. {PATTERN_OUTPUT}")
    print(f"2. {SUMMARY_OUTPUT}")

    print("\nMovement pattern analysis completed!")


if __name__ == "__main__":
    main()
