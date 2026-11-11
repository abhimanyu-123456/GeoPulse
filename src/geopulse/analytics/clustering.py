
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

MOVEMENT_FILE = DATA_DIR / "device_movement_summary.csv"

PATTERN_FILE = DATA_DIR / "device_pattern_summary.csv"

ASSIGNMENT_OUTPUT = DATA_DIR / "device_clusters.csv"

PROFILE_OUTPUT = DATA_DIR / "cluster_profiles.csv"


# --------------------------------------------------
# LOAD DEVICE SUMMARIES
# --------------------------------------------------

def load_device_data():

    if not MOVEMENT_FILE.exists():
        raise FileNotFoundError(
            f"Movement summary not found: {MOVEMENT_FILE}"
        )

    if not PATTERN_FILE.exists():
        raise FileNotFoundError(
            f"Pattern summary not found: {PATTERN_FILE}"
        )

    movement = pd.read_csv(MOVEMENT_FILE)

    patterns = pd.read_csv(PATTERN_FILE)

    df = movement.merge(
        patterns,
        on="DeviceID",
        how="inner",
        suffixes=("_movement", "_pattern")
    )

    if df.empty:
        raise ValueError(
            "No matching devices found in the summary files."
        )

    print(f"Devices loaded: {len(df):,}")

    return df


# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

def prepare_features(df):

    df = df.copy()

    # Number of valid intervals for each device
    valid_intervals = (
        df["GPS_Observations"] - 1
    ).clip(lower=0)

    # Convert category counts into proportions
    count_columns = {
        "Low_Speed_Rate": "Low_Speed_Count",
        "Moderate_Speed_Rate": "Moderate_Speed_Count",
        "Faster_Movement_Rate": "Faster_Movement_Count",
        "High_Speed_Anomaly_Rate": "High_Speed_Anomaly_Count"
    }

    for rate_column, count_column in count_columns.items():

        df[rate_column] = (
            df[count_column]
            .div(valid_intervals.replace(0, np.nan))
        )

    feature_columns = [
        "Total_Distance_KM",
        "Average_Speed_KMH",
        "Maximum_Speed_KMH",
        "Average_Interval_Minutes",
        "GPS_Observations",
        "Low_Speed_Rate",
        "Moderate_Speed_Rate",
        "Faster_Movement_Rate",
        "High_Speed_Anomaly_Rate"
    ]

    features = df[feature_columns].copy()

    # Make numeric values consistent
    features = features.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Remove negative or infinite values
    features = features.replace(
        [np.inf, -np.inf],
        np.nan
    )

    if (features < 0).any().any():
        raise ValueError(
            "Negative values found in clustering features."
        )

    # Log transformation reduces the effect of highly
    # skewed distance, speed and time measurements.
    log_columns = [
        "Total_Distance_KM",
        "Average_Speed_KMH",
        "Maximum_Speed_KMH",
        "Average_Interval_Minutes",
        "GPS_Observations"
    ]

    features[log_columns] = np.log1p(
        features[log_columns]
    )

    return features, feature_columns


# --------------------------------------------------
# PREPROCESS FEATURES
# --------------------------------------------------

def scale_features(features):

    imputer = SimpleImputer(
        strategy="median"
    )

    scaler = StandardScaler()

    imputed_features = imputer.fit_transform(
        features
    )

    scaled_features = scaler.fit_transform(
        imputed_features
    )

    return scaled_features


# --------------------------------------------------
# FIND BEST NUMBER OF CLUSTERS
# --------------------------------------------------

def find_best_clusters(scaled_features):

    results = []

    best_score = -1
    best_k = None
    best_model = None

    print("\nCLUSTER EVALUATION")
    print("-" * 45)

    for k in range(2, 7):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(
            scaled_features
        )

        score = silhouette_score(
            scaled_features,
            labels
        )

        results.append({
            "Number_of_Clusters": k,
            "Silhouette_Score": score
        })

        print(
            f"K = {k} | Silhouette Score = {score:.4f}"
        )

        if score > best_score:

            best_score = score
            best_k = k
            best_model = model

    print("\nBEST CLUSTER CONFIGURATION")
    print(f"Number of clusters: {best_k}")
    print(f"Silhouette score: {best_score:.4f}")

    return best_model, best_k, results


# --------------------------------------------------
# CREATE CLUSTER PROFILES
# --------------------------------------------------

def create_cluster_profiles(df):

    profile = (
        df.groupby("Cluster")
        .agg(
            Device_Count=("DeviceID", "count"),
            Average_Distance_KM=(
                "Total_Distance_KM", "mean"
            ),
            Average_Speed_KMH=(
                "Average_Speed_KMH", "mean"
            ),
            Average_Maximum_Speed_KMH=(
                "Maximum_Speed_KMH", "mean"
            ),
            Average_Observations=(
                "GPS_Observations", "mean"
            ),
            Average_Interval_Minutes=(
                "Average_Interval_Minutes", "mean"
            ),
            Average_High_Speed_Anomaly_Rate=(
                "High_Speed_Anomaly_Rate", "mean"
            )
        )
        .reset_index()
    )

    return profile.round(3)



# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\nGEO PULSE - K-MEANS CLUSTERING")
    print("=" * 50)

    # Load device summaries
    df = load_device_data()

    # Prepare machine-learning features
    features, feature_columns = prepare_features(df)

    # Copy engineered rate features into the original
    # dataframe so cluster profiles can access them.
    rate_columns = [
        "Low_Speed_Rate",
        "Moderate_Speed_Rate",
        "Faster_Movement_Rate",
        "High_Speed_Anomaly_Rate"
    ]

    for column in rate_columns:
        df[column] = features[column]

    print(
        f"Clustering features: {len(feature_columns)}"
    )

    # Scale features
    scaled_features = scale_features(features)

    print(
        f"Scaled feature matrix: {scaled_features.shape}"
    )

    # Find the best cluster configuration
    model, best_k, results = find_best_clusters(
        scaled_features
    )

    # Assign cluster labels
    df["Cluster"] = model.labels_

    # Create cluster profiles
    profiles = create_cluster_profiles(df)

    # Save evaluation results
    evaluation = pd.DataFrame(results)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        ASSIGNMENT_OUTPUT,
        index=False
    )

    profiles.to_csv(
        PROFILE_OUTPUT,
        index=False
    )

    evaluation.to_csv(
        DATA_DIR / "clustering_evaluation.csv",
        index=False
    )

    print("\nCLUSTER DISTRIBUTION")
    print("-" * 45)

    print(
        df["Cluster"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nCLUSTER PROFILES")
    print(profiles.to_string(index=False))

    print("\nOUTPUT FILES")
    print(f"1. {ASSIGNMENT_OUTPUT}")
    print(f"2. {PROFILE_OUTPUT}")
    print(
        f"3. {DATA_DIR / 'clustering_evaluation.csv'}"
    )

    print("\nK-MEANS CLUSTERING COMPLETED!")


if __name__ == "__main__":
    main()
