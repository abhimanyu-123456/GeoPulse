
import pandas as pd
import pytest

from dashboard.utils.data_loader import (
    load_dashboard_data,
    load_csv,
    DataLoadError
)

def test_dashboard_data_loads():

    data = load_dashboard_data()

    assert "movement_metrics" in data
    assert "movement_patterns" in data
    assert "device_clusters" in data
    assert "cluster_profiles" in data
    assert "clustering_evaluation" in data

def test_dashboard_data_is_not_empty():

    data = load_dashboard_data()

    assert not data["movement_metrics"].empty
    assert not data["device_clusters"].empty
    assert not data["cluster_profiles"].empty

def test_cluster_assignments_exist():

    data = load_dashboard_data()

    clusters = data["device_clusters"]

    assert clusters["Cluster"].notna().all()

def test_silhouette_scores_are_finite():

    data = load_dashboard_data()

    scores = data["clustering_evaluation"]["Silhouette_Score"]

    assert scores.notna().all()
    assert scores.map(pd.notna).all()

def test_missing_csv_raises_error():

    with pytest.raises(DataLoadError):

        load_csv("missing_dashboard_file.csv")