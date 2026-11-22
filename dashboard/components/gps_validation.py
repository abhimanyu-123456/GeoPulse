
"""
GeoPulse - Advanced GPS Data Validation

Validates coordinate ranges, numeric measurements,
timestamps, and completeness of synthetic GPS datasets.

License: GPL-3.0-only. See LICENSE.
"""

import pandas as pd


def validate_coordinates(df):
    """Validate available latitude and longitude columns."""

    results = {}

    coordinate_rules = {
        "Latitude": (-90, 90),
        "Longitude": (-180, 180),
    }

    for column, (minimum, maximum) in coordinate_rules.items():
        if column not in df.columns:
            results[column] = {
                "status": "Not Available",
                "invalid_count": None,
            }
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        invalid = values.isna() | ~values.between(minimum, maximum)

        results[column] = {
            "status": "Review Required" if invalid.any() else "Passed",
            "invalid_count": int(invalid.sum()),
        }

    return results


def validate_measurements(df):
    """Check GPS movement measurements for invalid values."""

    results = {}

    for column in ("Distance_KM", "Speed_KMH"):
        if column not in df.columns:
            results[column] = {
                "status": "Not Available",
                "invalid_count": None,
            }
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        invalid = values.isna() | (values < 0)

        results[column] = {
            "status": "Review Required" if invalid.any() else "Passed",
            "invalid_count": int(invalid.sum()),
        }

    return results


def calculate_completeness(df):
    """Calculate the percentage of nonmissing data cells."""

    if df.empty or len(df.columns) == 0:
        return None

    total_cells = df.shape[0] * df.shape[1]
    valid_cells = int(df.notna().sum().sum())

    return round((valid_cells / total_cells) * 100, 2)


def calculate_quality_score(df):
    """
    Calculate a diagnostic quality score.

    Score = percentage of valid cells across available
    columns, accounting for missing values, coordinate
    ranges, nonnegative movement measurements, and dates.

    This is a heuristic, not a measure of GPS accuracy.
    """

    if df.empty or len(df.columns) == 0:
        return None

    valid = df.notna().copy()

    coordinate_rules = {
        "Latitude": (-90, 90),
        "Longitude": (-180, 180),
    }

    for column, (minimum, maximum) in coordinate_rules.items():
        if column in df.columns:
            values = pd.to_numeric(df[column], errors="coerce")
            valid[column] = values.between(minimum, maximum)

    for column in ("Distance_KM", "Speed_KMH"):
        if column in df.columns:
            values = pd.to_numeric(df[column], errors="coerce")
            valid[column] = values.notna() & (values >= 0)

    if "Timestamp" in df.columns:
        timestamps = pd.to_datetime(
            df["Timestamp"],
            errors="coerce",
        )
        valid["Timestamp"] = timestamps.notna()

    total_cells = valid.size
    valid_cells = int(valid.to_numpy().sum())

    return round(100 * valid_cells / total_cells, 2)


def generate_validation_report(df):
    """Return a structured validation report."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    return {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "completeness_percentage": calculate_completeness(df),
        "quality_score": calculate_quality_score(df),
        "coordinates": validate_coordinates(df),
        "measurements": validate_measurements(df),
    }
