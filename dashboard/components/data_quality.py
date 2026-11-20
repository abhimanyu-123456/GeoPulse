
"""
GeoPulse - Data Quality and Validation Module

Provides data-quality checks for GPS movement analytics
datasets and displays validation results in Streamlit.
"""

import pandas as pd
import streamlit as st


def get_dataset_quality(df, dataset_name):
    """Calculate basic quality statistics for a dataset."""

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()

    total_rows = len(df)
    total_columns = len(df.columns)

    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    missing_percentage = (
        (missing_values / (total_rows * total_columns)) * 100
        if total_rows > 0 and total_columns > 0
        else 0
    )

    return {
        "Dataset": dataset_name,
        "Total Records": total_rows,
        "Total Columns": total_columns,
        "Missing Values": missing_values,
        "Duplicate Rows": duplicate_rows,
        "Missing (%)": round(missing_percentage, 2),
    }


def validate_numeric_column(df, column):
    """Identify invalid or negative numeric observations."""

    if column not in df.columns:
        return 0, 0

    values = pd.to_numeric(df[column], errors="coerce")

    invalid_values = int(values.isna().sum())
    negative_values = int((values.dropna() < 0).sum())

    return invalid_values, negative_values


def validate_timestamps(df):
    """Check timestamp availability and invalid timestamp values."""

    if "Timestamp" not in df.columns:
        return 0, None, None

    timestamps = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    invalid_count = int(timestamps.isna().sum())

    valid_timestamps = timestamps.dropna()

    if valid_timestamps.empty:
        return invalid_count, None, None

    return (
        invalid_count,
        valid_timestamps.min(),
        valid_timestamps.max()
    )


def display_data_quality(data):
    """Display data-quality metrics and validation results."""

    st.header("Data Quality & Validation")

    st.write(
        "This section evaluates the completeness, consistency "
        "and reliability of the processed GeoPulse datasets."
    )

    # Collect available datasets.
    datasets = {
        "Movement Metrics": data.get(
            "movement_metrics", pd.DataFrame()
        ),
        "Movement Patterns": data.get(
            "movement_patterns", pd.DataFrame()
        ),
        "Device Clusters": data.get(
            "device_clusters", pd.DataFrame()
        ),
        "Cluster Profiles": data.get(
            "cluster_profiles", pd.DataFrame()
        ),
        "Clustering Evaluation": data.get(
            "clustering_evaluation", pd.DataFrame()
        ),
    }

    # Generate dataset quality summaries.
    quality_results = []

    for name, df in datasets.items():
        quality_results.append(
            get_dataset_quality(df, name)
        )

    quality_df = pd.DataFrame(quality_results)

    # Calculate overall statistics.
    total_records = int(
        quality_df["Total Records"].sum()
    )

    total_missing = int(
        quality_df["Missing Values"].sum()
    )

    total_duplicates = int(
        quality_df["Duplicate Rows"].sum()
    )

    # Display summary metrics.
    st.subheader("Overall Data Quality Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Dataset Records", f"{total_records:,}")
    col2.metric("Missing Values", f"{total_missing:,}")
    col3.metric("Duplicate Rows", f"{total_duplicates:,}")

    st.divider()

    # Dataset-level quality table.
    st.subheader("Dataset Quality Report")

    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Detailed movement metrics validation.
    st.subheader("GPS Movement Data Validation")

    movement_df = datasets["Movement Metrics"]

    if movement_df.empty:
        st.warning("Movement metrics dataset is empty.")
    else:
        validation_results = []

        for column in ["Distance_KM", "Speed_KMH"]:
            invalid, negative = validate_numeric_column(
                movement_df, column
            )

            validation_results.append({
                "Column": column,
                "Invalid Values": invalid,
                "Negative Values": negative,
                "Status": (
                    "Passed"
                    if invalid == 0 and negative == 0
                    else "Review Required"
                )
            })

        validation_df = pd.DataFrame(validation_results)

        st.dataframe(
            validation_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Timestamp validation.
    st.subheader("Timestamp Coverage")

    timestamp_df = datasets["Movement Metrics"]

    invalid_dates, earliest, latest = validate_timestamps(
        timestamp_df
    )

    date_col1, date_col2, date_col3 = st.columns(3)

    date_col1.metric(
        "Invalid Timestamps",
        f"{invalid_dates:,}"
    )

    date_col2.metric(
        "First Observation",
        str(earliest.date()) if earliest is not None else "N/A"
    )

    date_col3.metric(
        "Last Observation",
        str(latest.date()) if latest is not None else "N/A"
    )

    st.divider()

    # Overall validation status.
    negative_total = 0
    invalid_numeric_total = 0

    if not movement_df.empty:
        for column in ["Distance_KM", "Speed_KMH"]:
            invalid, negative = validate_numeric_column(
                movement_df, column
            )

            invalid_numeric_total += invalid
            negative_total += negative

    validation_passed = (
        total_missing == 0
        and total_duplicates == 0
        and invalid_dates == 0
        and invalid_numeric_total == 0
        and negative_total == 0
    )

    st.subheader("Final Data Quality Status")

    if validation_passed:
        st.success(
            "All available datasets passed the configured "
            "data-quality checks."
        )
    else:
        st.warning(
            "Some data-quality issues were detected. "
            "Review the reports above before further analysis."
        )

    st.caption(
        "GeoPulse Data Quality Module | "
        "Automated Dataset Validation"
    )
