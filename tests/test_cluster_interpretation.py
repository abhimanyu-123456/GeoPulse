
import pandas as pd
import pytest

from geopulse.analytics.cluster_interpretation import (
    interpret_clusters,
    load_cluster_profiles,
    save_interpretations
)


def sample_profiles():

    return pd.DataFrame({

        "Cluster": [0, 1, 2],

        "Device_Count": [100, 50, 75],

        "Average_Distance_KM": [1.0, 10.0, 100.0],

        "Average_Speed_KMH": [0.1, 1.0, 10.0],

        "Average_Observations": [4.0, 1.0, 5.0]

    })


def test_every_cluster_receives_interpretation():

    df = sample_profiles()

    result = interpret_clusters(df)

    assert "Interpretation" in result.columns

    assert result["Interpretation"].notna().all()

    assert len(result) == 3


def test_insufficient_observations_are_identified():

    df = sample_profiles()

    result = interpret_clusters(df)

    cluster = result[
        result["Cluster"] == 1
    ].iloc[0]

    assert (
        cluster["Interpretation"]
        == "Insufficient observation data"
    )


def test_low_movement_is_identified():

    df = sample_profiles()

    result = interpret_clusters(df)

    cluster = result[
        result["Cluster"] == 0
    ].iloc[0]

    assert (
        cluster["Interpretation"]
        == "Low observed movement"
    )


def test_interpretation_file_is_saved(tmp_path):

    df = interpret_clusters(sample_profiles())

    output = tmp_path / "interpretation.csv"

    save_interpretations(df, output)

    assert output.exists()

    saved = pd.read_csv(output)

    assert "Interpretation" in saved.columns


def test_missing_cluster_file_raises_error(tmp_path):

    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):

        load_cluster_profiles(missing_file)
