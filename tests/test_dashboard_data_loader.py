
import pandas as pd
import pytest

from dashboard.utils import data_loader


def test_load_csv_successfully(tmp_path, monkeypatch):
    """Check that a valid CSV file loads successfully."""

    sample_data = pd.DataFrame({
        "DeviceID": ["D001", "D002"],
        "Speed_KMH": [25.5, 30.2]
    })

    sample_data.to_csv(
        tmp_path / "sample.csv",
        index=False
    )

    monkeypatch.setattr(
        data_loader,
        "DATA_DIR",
        tmp_path
    )

    result = data_loader.load_csv(
        "sample.csv",
        ["DeviceID", "Speed_KMH"]
    )

    assert len(result) == 2
    assert "DeviceID" in result.columns


def test_load_csv_missing_file(tmp_path, monkeypatch):
    """Check that missing files produce a clear error."""

    monkeypatch.setattr(
        data_loader,
        "DATA_DIR",
        tmp_path
    )

    with pytest.raises(data_loader.DataLoadError):
        data_loader.load_csv("missing.csv")


def test_load_csv_missing_columns(tmp_path, monkeypatch):
    """Check that missing required columns are detected."""

    sample_data = pd.DataFrame({
        "DeviceID": ["D001"]
    })

    sample_data.to_csv(
        tmp_path / "sample.csv",
        index=False
    )

    monkeypatch.setattr(
        data_loader,
        "DATA_DIR",
        tmp_path
    )

    with pytest.raises(data_loader.DataLoadError):
        data_loader.load_csv(
            "sample.csv",
            ["DeviceID", "Speed_KMH"]
        )
