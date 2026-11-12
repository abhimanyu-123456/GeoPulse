
from pathlib import Path

import pandas as pd
import pytest


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def test_raw_gps_dataset_exists():
    """Check that the generated GPS dataset exists."""
    file_path = RAW_DIR / "gps_pings.csv"

    assert file_path.exists(), "Raw GPS dataset is missing"


def test_raw_gps_dataset_quality():
    """Check the expected size and essential GPS columns."""
    df = pd.read_csv(RAW_DIR / "gps_pings.csv")

    assert len(df) == 10_000
    assert {
        "DeviceID",
        "Lat",
        "Long",
        "Timestamp",
    }.issubset(df.columns)

    assert df["DeviceID"].nunique() == 1_994
    assert df["Lat"].between(-90, 90).all()
    assert df["Long"].between(-180, 180).all()
    assert not df.isnull().any().any()


def test_movement_metrics_output():
    """Check the movement analytics output."""
    file_path = PROCESSED_DIR / "movement_metrics.csv"

    assert file_path.exists(), "Movement metrics file is missing"

    df = pd.read_csv(file_path)

    required_columns = {
        "DeviceID",
        "Timestamp",
        "Distance_KM",
        "Speed_KMH",
        "Time_Difference_Seconds",
    }

    assert required_columns.issubset(df.columns)
    assert len(df) == 10_000
    assert (df["Distance_KM"] >= 0).all()

    valid_speeds = df["Speed_KMH"].dropna()
    assert (valid_speeds >= 0).all()


def test_movement_patterns_output():
    """Check that movement categories were generated."""
    file_path = PROCESSED_DIR / "movement_patterns.csv"

    assert file_path.exists(), "Movement patterns file is missing"

    df = pd.read_csv(file_path)

    assert "DeviceID" in df.columns
    assert "Speed_Category" in df.columns
    assert len(df) == 10_000

    assert df["Speed_Category"].notna().all()

    expected_categories = {
        "Low Speed",
        "Moderate Speed",
        "Insufficient Data",
        "Faster Movement",
        "Unusually High Speed",
    }

    assert set(df["Speed_Category"].unique()).issubset(
        expected_categories
    )


def test_device_clustering_output():
    """Check device assignments and cluster profiles."""
    assignments_path = PROCESSED_DIR / "device_clusters.csv"
    profiles_path = PROCESSED_DIR / "cluster_profiles.csv"

    assert assignments_path.exists()
    assert profiles_path.exists()

    assignments = pd.read_csv(assignments_path)
    profiles = pd.read_csv(profiles_path)

    assert "DeviceID" in assignments.columns
    assert "Cluster" in assignments.columns
    assert assignments["DeviceID"].nunique() == 1_994

    assert assignments["Cluster"].notna().all()
    assert assignments["Cluster"].nunique() == 5

    assert "Device_Count" in profiles.columns
    assert len(profiles) == 5
    assert profiles["Device_Count"].sum() == 1_994


def test_clustering_evaluation_output():
    """Check the saved silhouette evaluation results."""
    file_path = PROCESSED_DIR / "clustering_evaluation.csv"

    assert file_path.exists()

    df = pd.read_csv(file_path)

    assert {
        "Number_of_Clusters",
        "Silhouette_Score",
    }.issubset(df.columns)

    assert len(df) == 5
    assert df["Silhouette_Score"].between(-1, 1).all()

    best_row = df.loc[df["Silhouette_Score"].idxmax()]
    assert best_row["Number_of_Clusters"] == 5


def test_visualization_files_exist():
    """Check that all five expected charts were generated."""
    expected_files = [
        "cluster_distribution.png",
        "silhouette_scores.png",
        "average_distance.png",
        "average_speed.png",
        "distance_vs_speed.png",
    ]

    for filename in expected_files:
        file_path = FIGURES_DIR / filename

        assert file_path.exists(), f"Missing chart: {filename}"
        assert file_path.stat().st_size > 0, (
            f"Chart is empty: {filename}"
        )
