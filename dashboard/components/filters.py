
"""
GeoPulse - Dashboard Filters
"""

import streamlit as st
import pandas as pd

def apply_filters(data):

    filtered = {
        key: value.copy()
        for key, value in data.items()
    }

    devices = filtered["device_clusters"]
    patterns = filtered["movement_patterns"]
    movement = filtered["movement_metrics"]
    profiles = filtered["cluster_profiles"]

    st.sidebar.header("Dashboard Filters")

    # -----------------------------------------------
    # CLUSTER FILTER
    # -----------------------------------------------

    cluster_options = sorted(
        devices["Cluster"].dropna().unique().tolist()
    )

    selected_cluster = st.sidebar.selectbox(
        "Select Cluster",
        ["All"] + cluster_options
    )

    if selected_cluster != "All":

        devices = devices[
            devices["Cluster"] == selected_cluster
        ]

        selected_ids = devices["DeviceID"].unique()

        patterns = patterns[
            patterns["DeviceID"].isin(selected_ids)
        ]

        movement = movement[
            movement["DeviceID"].isin(selected_ids)
        ]

        profiles = profiles[
            profiles["Cluster"] == selected_cluster
        ]

    # -----------------------------------------------
    # DEVICE FILTER
    # -----------------------------------------------

    device_options = sorted(
        devices["DeviceID"].dropna().unique().tolist()
    )

    selected_device = st.sidebar.selectbox(
        "Select Device",
        ["All"] + device_options
    )

    if selected_device != "All":

        devices = devices[
            devices["DeviceID"] == selected_device
        ]

        patterns = patterns[
            patterns["DeviceID"] == selected_device
        ]

        movement = movement[
            movement["DeviceID"] == selected_device
        ]

    # -----------------------------------------------
    # MOVEMENT CATEGORY FILTER
    # -----------------------------------------------

    category_options = sorted(
        patterns["Speed_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.sidebar.selectbox(
        "Movement Category",
        ["All"] + category_options
    )

    if selected_category != "All":

        patterns = patterns[
            patterns["Speed_Category"] == selected_category
        ]

    # -----------------------------------------------
    # DATE FILTER
    # -----------------------------------------------

    st.sidebar.subheader("Date Range")

    timestamp_values = movement["Timestamp"].dropna()

    if not timestamp_values.empty:

        min_date = timestamp_values.min().date()
        max_date = timestamp_values.max().date()

        selected_dates = st.sidebar.date_input(
            "Select dates",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

            start_date, end_date = selected_dates

            movement = movement[
                movement["Timestamp"].dt.date.between(
                    start_date,
                    end_date
                )
            ]

            patterns = patterns[
                patterns["Timestamp"].dt.date.between(
                    start_date,
                    end_date
                )
            ]

    filtered["device_clusters"] = devices
    filtered["movement_patterns"] = patterns
    filtered["movement_metrics"] = movement
    filtered["cluster_profiles"] = profiles

    return filtered