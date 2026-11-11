
import numpy as np
import pandas as pd

from geopulse.analytics.clustering import (
    prepare_features,
    scale_features,
)

def test_feature_preparation_returns_expected_columns():
    df = pd.DataFrame({
        "Total_Distance_KM": [10.0, 20.0, 30.0],
        "Average_Speed_KMH": [1.0, 2.0, 3.0],
        "Maximum_Speed_KMH": [2.0, 4.0, 6.0],
        "Average_Interval_Minutes": [30.0, 60.0, 90.0],
        "GPS_Observations": [3, 4, 5],
        "Low_Speed_Count": [1, 2, 2],
        "Moderate_Speed_Count": [1, 1, 2],
        "Faster_Movement_Count": [1, 1, 1],
        "High_Speed_Anomaly_Count": [0, 0, 0],
    })

    features, columns = prepare_features(df)

    assert len(columns) == 9
    assert features.shape == (3, 9)
    assert np.isfinite(
        features.to_numpy(dtype=float)
    ).all()

def test_scaled_features_are_finite():
    features = pd.DataFrame({
        "feature_a": [1.0, 2.0, 3.0],
        "feature_b": [10.0, 20.0, 30.0],
    })

    scaled = scale_features(features)

    assert scaled.shape == (3, 2)
    assert np.isfinite(scaled).all()
    assert scaled.mean(axis=0) == pytest_approx_zero()

def pytest_approx_zero():
    # Return a pytest approximation without hiding
    # the expected near-zero floating-point tolerance.
    import pytest

    return pytest.approx([0.0, 0.0], abs=1e-9)