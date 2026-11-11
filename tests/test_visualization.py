
import pandas as pd

from geopulse.analytics import visualization

def test_all_visualizations_are_generated(tmp_path, monkeypatch):
    monkeypatch.setattr(
        visualization,
        "OUTPUT_DIR",
        tmp_path,
    )

    devices = pd.DataFrame({
        "Cluster": [0, 0, 1, 1, 2],
    })

    profiles = pd.DataFrame({
        "Cluster": [0, 1, 2],
        "Device_Count": [2, 2, 1],
        "Average_Distance_KM": [10.0, 20.0, 30.0],
        "Average_Speed_KMH": [1.0, 3.0, 5.0],
    })

    evaluation = pd.DataFrame({
        "Number_of_Clusters": [2, 3, 4, 5, 6],
        "Silhouette_Score": [0.30, 0.36, 0.39, 0.41, 0.35],
    })

    visualization.plot_cluster_distribution(devices)
    visualization.plot_silhouette_scores(evaluation)
    visualization.plot_average_distance(profiles)
    visualization.plot_average_speed(profiles)
    visualization.plot_device_movement(profiles)

    expected_files = [
        "cluster_distribution.png",
        "silhouette_scores.png",
        "average_distance.png",
        "average_speed.png",
        "distance_vs_speed.png",
    ]

    for filename in expected_files:
        output_file = tmp_path / filename
        assert output_file.exists()
        assert output_file.stat().st_size > 0