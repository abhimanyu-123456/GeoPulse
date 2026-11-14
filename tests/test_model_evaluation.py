
import numpy as np
import pandas as pd
import pytest

from geopulse.analytics.model_evaluation import (
    calculate_metrics,
    evaluate_model,
    INPUT_FILE
)


def test_evaluation_metrics_are_calculated():

    features = np.array([

        [1.0, 1.0],
        [1.2, 1.1],
        [0.8, 0.9],

        [8.0, 8.0],
        [8.2, 8.1],
        [7.8, 7.9]

    ])

    labels = [0, 0, 0, 1, 1, 1]

    results = calculate_metrics(
        features,
        labels
    )

    assert "Silhouette_Score" in results

    assert "Davies_Bouldin_Score" in results

    assert "Calinski_Harabasz_Score" in results


def test_evaluation_scores_are_finite():

    features = np.array([

        [1.0, 1.0],
        [1.2, 1.1],
        [0.8, 0.9],

        [8.0, 8.0],
        [8.2, 8.1],
        [7.8, 7.9]

    ])

    labels = [0, 0, 0, 1, 1, 1]

    results = calculate_metrics(
        features,
        labels
    )

    for value in results.values():

        assert np.isfinite(value)


def test_evaluation_requires_multiple_clusters():

    features = np.array([

        [1.0, 1.0],
        [1.2, 1.1],
        [0.8, 0.9]

    ])

    labels = [0, 0, 0]

    with pytest.raises(ValueError):

        calculate_metrics(
            features,
            labels
        )


def test_existing_devices_have_cluster_assignments():

    df = pd.read_csv(INPUT_FILE)

    assert "Cluster" in df.columns

    assert df["Cluster"].notna().all()


def test_model_evaluation_file_is_generated(tmp_path):

    if not INPUT_FILE.exists():

        pytest.skip(
            "Existing clustering dataset is unavailable."
        )

    output = tmp_path / "model_evaluation.csv"

    results, features = evaluate_model(
        input_path=INPUT_FILE,
        output_path=output
    )

    assert output.exists()

    assert len(features) == 9

    assert "Overall" in results["Evaluation_Type"].values

    assert "Cluster_Size" in results["Evaluation_Type"].values

    overall = results[
        results["Evaluation_Type"] == "Overall"
    ]

    assert len(overall) == 3

    assert np.isfinite(
        overall["Value"].astype(float)
    ).all()

    distribution = results[
        results["Evaluation_Type"] == "Cluster_Size"
    ]

    assert distribution["Device_Count"].sum() == len(pd.read_csv(INPUT_FILE))
