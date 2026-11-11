
import pandas as pd

from geopulse.geospatial.movement_patterns import (
    classify_speed,
    identify_stationary_periods,
)

def test_speed_classification():
    df = pd.DataFrame({
        "Speed_KMH": [
            0.2,
            2.0,
            8.0,
            100.0,
            float("nan"),
        ],
    })

    result, threshold = classify_speed(df)

    assert result.loc[0, "Speed_Category"] == "Low Speed"
    assert result.loc[1, "Speed_Category"] == "Moderate Speed"
    assert result.loc[2, "Speed_Category"] == "Faster Movement"
    assert (
        result.loc[3, "Speed_Category"]
        == "Unusually High Speed"
    )
    assert (
        result.loc[4, "Speed_Category"]
        == "Insufficient Data"
    )
    assert threshold >= 0

def test_potential_stationary_observation():
    df = pd.DataFrame({
        "Distance_KM": [0.01, 0.01, 0.01],
        "Time_Difference_Seconds": [
            600,
            3600,
            float("nan"),
        ],
    })

    result = identify_stationary_periods(df)

    assert bool(result.loc[0, "Potential_Stationary"]) is True
    assert bool(result.loc[1, "Potential_Stationary"]) is False
    assert bool(result.loc[2, "Potential_Stationary"]) is False