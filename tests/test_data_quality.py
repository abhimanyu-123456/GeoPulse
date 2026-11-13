import pandas as pd

def test_valid_coordinates_are_within_geographic_bounds():
    df = pd.DataFrame(
        {
            "Lat": [23.25, 23.26],
            "Long": [77.40, 77.41],
        }
    )

    assert df["Lat"].between(-90, 90).all()
    assert df["Long"].between(-180, 180).all()

def test_invalid_coordinates_are_detected():
    df = pd.DataFrame(
        {
            "Lat": [23.25, 95.0],
            "Long": [77.40, 200.0],
        }
    )

    invalid = (
        ~df["Lat"].between(-90, 90)
        | ~df["Long"].between(-180, 180)
    )

    assert invalid.sum() == 1

def test_duplicate_rows_can_be_detected():
    df = pd.DataFrame(
        {
            "DeviceID": ["A", "A", "B"],
            "Lat": [23.2, 23.2, 23.3],
            "Long": [77.4, 77.4, 77.5],
            "Timestamp": [
                "2026-01-01 10:00:00",
                "2026-01-01 10:00:00",
                "2026-01-01 11:00:00",
            ],
        }
    )

    assert df.duplicated().sum() == 1

def test_timestamps_can_be_parsed():
    timestamps = pd.to_datetime(
        pd.Series(["2026-01-01 10:00:00", "invalid"]),
        errors="coerce",
    )

    assert timestamps.notna().sum() == 1
