
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = ROOT_DIR / "data" / "processed"

OUTPUT_DIR = ROOT_DIR / "reports" / "figures"

DEVICE_FILE = DATA_DIR / "device_clusters.csv"
PROFILE_FILE = DATA_DIR / "cluster_profiles.csv"
EVALUATION_FILE = DATA_DIR / "clustering_evaluation.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_visualization_data():

    devices = pd.read_csv(DEVICE_FILE)
    profiles = pd.read_csv(PROFILE_FILE)
    evaluation = pd.read_csv(EVALUATION_FILE)

    print("Visualization data loaded successfully.")
    print(f"Devices: {len(devices)}")
    print(f"Clusters: {len(profiles)}")

    return devices, profiles, evaluation


# --------------------------------------------------
# CREATE OUTPUT DIRECTORY
# --------------------------------------------------

def create_output_directory():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# --------------------------------------------------
# 1. CLUSTER DISTRIBUTION
# --------------------------------------------------

def plot_cluster_distribution(devices):

    counts = (
        devices["Cluster"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(9, 5))

    plt.bar(
        counts.index.astype(str),
        counts.values
    )

    plt.title("GeoPulse - Device Distribution by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Number of Devices")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "cluster_distribution.png",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# 2. SILHOUETTE SCORE COMPARISON
# --------------------------------------------------

def plot_silhouette_scores(evaluation):

    plt.figure(figsize=(9, 5))

    plt.plot(
        evaluation["Number_of_Clusters"],
        evaluation["Silhouette_Score"],
        marker="o"
    )

    plt.title("K-Means Cluster Evaluation")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.xticks(
        evaluation["Number_of_Clusters"]
    )

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "silhouette_scores.png",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# 3. AVERAGE DISTANCE BY CLUSTER
# --------------------------------------------------

def plot_average_distance(profiles):

    plt.figure(figsize=(9, 5))

    plt.bar(
        profiles["Cluster"].astype(str),
        profiles["Average_Distance_KM"]
    )

    plt.title("Average Distance by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Average Distance (KM)")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "average_distance.png",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# 4. AVERAGE SPEED BY CLUSTER
# --------------------------------------------------

def plot_average_speed(profiles):

    plt.figure(figsize=(9, 5))

    plt.bar(
        profiles["Cluster"].astype(str),
        profiles["Average_Speed_KMH"]
    )

    plt.title("Average Movement Speed by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Average Speed (KM/H)")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "average_speed.png",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# 5. DEVICE MOVEMENT COMPARISON
# --------------------------------------------------

def plot_device_movement(profiles):

    plt.figure(figsize=(9, 6))

    plt.scatter(
        profiles["Average_Distance_KM"],
        profiles["Average_Speed_KMH"],
        s=profiles["Device_Count"] * 0.5,
        alpha=0.7
    )

    for _, row in profiles.iterrows():

        plt.annotate(
            f"Cluster {int(row['Cluster'])}",
            (
                row["Average_Distance_KM"],
                row["Average_Speed_KMH"]
            )
        )

    plt.title("Distance vs Speed by Cluster")
    plt.xlabel("Average Distance (KM)")
    plt.ylabel("Average Speed (KM/H)")
    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "distance_vs_speed.png",
        dpi=300
    )

    plt.close()


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    print("\nGEOPULSE - DATA VISUALIZATION")
    print("=" * 50)

    create_output_directory()

    devices, profiles, evaluation = (
        load_visualization_data()
    )

    print("\nGenerating visualizations...")

    plot_cluster_distribution(devices)
    print("1. Cluster distribution completed.")

    plot_silhouette_scores(evaluation)
    print("2. Silhouette score chart completed.")

    plot_average_distance(profiles)
    print("3. Average distance chart completed.")

    plot_average_speed(profiles)
    print("4. Average speed chart completed.")

    plot_device_movement(profiles)
    print("5. Distance vs speed chart completed.")

    print("\nOUTPUT DIRECTORY")
    print(OUTPUT_DIR)

    print("\nAll visualizations generated successfully!")


if __name__ == "__main__":
    main()
