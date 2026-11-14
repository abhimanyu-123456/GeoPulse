
"""
GeoPulse - Dashboard Data Loader

Loads and validates existing processed GPS analytics datasets.
"""

from pathlib import Path

import pandas as pd


# ==================================================
# PROJECT DIRECTORIES
# ==================================================

# dashboard/utils/data_loader.py
# parents[0] = dashboard/utils
# parents[1] = dashboard
# parents[2] = GeoPulse project root

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

RAW_DIR = PROJECT_ROOT / "data" / "raw"


# ==================================================
# CUSTOM EXCEPTION
# ==================================================

class DataLoadError(Exception):
    """Raised when dashboard data cannot be loaded."""


# ==================================================
# CSV LOADER
# ==================================================

def load_csv(filename, required_columns=None):
    """
    Load a CSV file and validate its required columns.
    """

    file_path = DATA_DIR / filename

    if not file_path.exists():

        raise DataLoadError(
            f"Required dataset is missing: {file_path}"
        )

    try:

        df = pd.read_csv(file_path)

    except (
        OSError,
        pd.errors.ParserError,
        UnicodeError,
        pd.errors.EmptyDataError,
    ) as error:

        raise DataLoadError(
            f"Unable to read {filename}: {error}"
        ) from error

    if required_columns:

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise DataLoadError(
                f"{filename} is missing columns: "
                f"{sorted(missing)}"
            )

    return df


# ==================================================
# DASHBOARD DATA LOADER
# ==================================================

def load_dashboard_data():
    """
    Load all datasets required by the GeoPulse dashboard.
    """

    data = {}

    # ----------------------------------------------
    # MOVEMENT METRICS
    # ----------------------------------------------

    data["movement_metrics"] = load_csv(
        "movement_metrics.csv",
        [
            "DeviceID",
            "Timestamp",
            "Distance_KM",
            "Speed_KMH",
        ],
    )

    # ----------------------------------------------
    # MOVEMENT PATTERNS
    # ----------------------------------------------

    data["movement_patterns"] = load_csv(
        "movement_patterns.csv",
        [
            "DeviceID",
            "Speed_Category",
        ],
    )

    # ----------------------------------------------
    # DEVICE CLUSTERS
    # ----------------------------------------------

    data["device_clusters"] = load_csv(
        "device_clusters.csv",
        [
            "DeviceID",
            "Cluster",
            "Total_Distance_KM",
            "Average_Speed_KMH",
        ],
    )

    # ----------------------------------------------
    # CLUSTER PROFILES
    # ----------------------------------------------

    data["cluster_profiles"] = load_csv(
        "cluster_profiles.csv",
        [
            "Cluster",
            "Device_Count",
            "Average_Distance_KM",
            "Average_Speed_KMH",
        ],
    )

    # ----------------------------------------------
    # CLUSTERING EVALUATION
    # ----------------------------------------------

    data["clustering_evaluation"] = load_csv(
        "clustering_evaluation.csv",
        [
            "Number_of_Clusters",
            "Silhouette_Score",
        ],
    )

    # ----------------------------------------------
    # OPTIONAL RAW GPS DATA
    # ----------------------------------------------

    raw_file = RAW_DIR / "gps_pings.csv"

    if raw_file.exists():

        try:

            data["raw_gps"] = pd.read_csv(raw_file)

        except (
            OSError,
            pd.errors.ParserError,
            UnicodeError,
            pd.errors.EmptyDataError,
        ) as error:

            raise DataLoadError(
                f"Unable to read raw GPS dataset: {error}"
            ) from error

    else:

        data["raw_gps"] = pd.DataFrame()

    # ----------------------------------------------
    # TIMESTAMP CONVERSION
    # ----------------------------------------------

    for key in [
        "movement_metrics",
        "movement_patterns",
    ]:

        if "Timestamp" in data[key].columns:

            data[key]["Timestamp"] = pd.to_datetime(
                data[key]["Timestamp"],
                errors="coerce",
            )

    # ----------------------------------------------
    # NUMERIC DATA CONVERSION
    # ----------------------------------------------

    numeric_columns = {

        "movement_metrics": [
            "Distance_KM",
            "Speed_KMH",
        ],

        "device_clusters": [
            "Cluster",
            "Total_Distance_KM",
            "Average_Speed_KMH",
        ],

        "cluster_profiles": [
            "Cluster",
            "Device_Count",
            "Average_Distance_KM",
            "Average_Speed_KMH",
        ],

        "clustering_evaluation": [
            "Number_of_Clusters",
            "Silhouette_Score",
        ],
    }

    for key, columns in numeric_columns.items():

        for column in columns:

            data[key][column] = pd.to_numeric(
                data[key][column],
                errors="coerce",
            )

    return data
