
import pandas as pd
import pytest

from geopulse.analytics import analytics_report


def sample_report_data():

    return {

        "gps": pd.DataFrame({

            "DeviceID": [
                "DEVICE_001",
                "DEVICE_002",
                "DEVICE_001"
            ]

        }),

        "movement": pd.DataFrame({

            "Distance_KM": [1.5, 2.0, 3.0],

            "Speed_KMH": [1.0, 2.0, 3.0]

        }),

        "patterns": pd.DataFrame({

            "Speed_Category": [
                "Low Speed",
                "Moderate Speed",
                "Low Speed"
            ]

        }),

        "clusters": pd.DataFrame({

            "Cluster": [0, 1, 0]

        }),

        "profiles": pd.DataFrame({

            "Cluster": [0, 1]

        }),

        "evaluation": pd.DataFrame({

            "Evaluation_Type": [
                "Overall",
                "Overall",
                "Overall"
            ],

            "Metric": [
                "Silhouette_Score",
                "Davies_Bouldin_Score",
                "Calinski_Harabasz_Score"
            ],

            "Value": [
                0.41,
                0.75,
                120.0
            ]

        })

    }


def test_analytics_report_is_generated():

    report = analytics_report.build_report(
        sample_report_data()
    )

    assert "GEOPULSE ANALYTICS SUMMARY" in report

    assert "Total GPS Records: 3" in report

    assert "Unique Devices: 2" in report

    assert "CLUSTERING RESULTS" in report

    assert "MODEL EVALUATION" in report


def test_report_contains_movement_categories():

    report = analytics_report.build_report(
        sample_report_data()
    )

    assert "Low Speed" in report

    assert "Moderate Speed" in report


def test_report_contains_evaluation_metrics():

    report = analytics_report.build_report(
        sample_report_data()
    )

    assert "Silhouette_Score" in report

    assert "Davies_Bouldin_Score" in report

    assert "Calinski_Harabasz_Score" in report


def test_report_is_saved(tmp_path):

    report = analytics_report.build_report(
        sample_report_data()
    )

    output = tmp_path / "analytics_summary.txt"

    analytics_report.save_report(
        report,
        output
    )

    assert output.exists()

    content = output.read_text(
        encoding="utf-8"
    )

    assert "GEOPULSE ANALYTICS SUMMARY" in content


def test_missing_input_file_raises_error(tmp_path, monkeypatch):

    monkeypatch.setattr(
        analytics_report,
        "RAW_DIR",
        tmp_path / "raw"
    )

    monkeypatch.setattr(
        analytics_report,
        "DATA_DIR",
        tmp_path / "processed"
    )

    with pytest.raises(FileNotFoundError):

        analytics_report.load_report_data()
