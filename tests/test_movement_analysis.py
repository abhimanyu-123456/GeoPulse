
import pandas as pd
import pytest

from geopy.distance import geodesic

from geopulse.geospatial.movement_analysis import (
    calculate_distance,
    perform_movement_analysis,
)

def test_distance_between_identical_coordinates():
    distance = geodesic(
        (23.2599, 77.4126),
        (23.2599, 77.4126),
    ).kilometers

    assert distance == pytest.approx(0.0)

def test_distance_between_different_coordinates():
    distance = geodesic(
        (23.2599, 77.4126),
        (23.2609, 77.4136),
    ).kilometers

    assert distance > 0

def test_first_observation_has_zero_distance():
    df = pd.DataFrame({
        "DeviceID": ["D001"],
        "Lat": [23.2599],
        "Long": [77.4126],
        "Timestamp": pd.to_datetime(
            ["2026-01-01 10:00:00"]
        ),
    })

    result = perform_movement_analysis(df)

    assert result.loc[0, "Distance_KM"] == pytest.approx(0.0)
    assert pd.isna(result.loc[0, "Speed_KMH"])

def test_speed_is_calculated_correctly():
    df = pd.DataFrame({
        "DeviceID": ["D001", "D001"],
        "Lat": [23.2599, 23.2609],
        "Long": [77.4126, 77.4136],
        "Timestamp": pd.to_datetime([
            "2026-01-01 10:00:00",
            "2026-01-01 11:00:00",
        ]),
    })

    result = perform_movement_analysis(df)

    expected_distance = geodesic(
        (23.2599, 77.4126),
        (23.2609, 77.4136),
    ).kilometers

    assert result.loc[1, "Distance_KM"] == pytest.approx(
        expected_distance
    )

    assert result.loc[1, "Time_Difference_Seconds"] == 3600

    assert result.loc[1, "Speed_KMH"] == pytest.approx(
        expected_distance
    )

def test_devices_are_analyzed_separately():
    df = pd.DataFrame({
        "DeviceID": ["D001", "D002"],
        "Lat": [23.2599, 23.2609],
        "Long": [77.4126, 77.4136],
        "Timestamp": pd.to_datetime([
            "2026-01-01 10:00:00",
            "2026-01-01 10:00:00",
        ]),
    })

    result = perform_movement_analysis(df)

    assert result["Distance_KM"].tolist() == pytest.approx(
        [0.0, 0.0]
    )
    assert result["Time_Difference_Seconds"].isna().all()