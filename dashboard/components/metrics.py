
"""
GeoPulse - Dashboard KPI Metrics
"""

import streamlit as st
import pandas as pd

def display_metrics(data):

    movement = data["movement_metrics"]
    clusters = data["device_clusters"]
    evaluation = data["clustering_evaluation"]
    raw_gps = data["raw_gps"]

    # Total GPS observations
    if not raw_gps.empty:
        total_records = len(raw_gps)
    else:
        total_records = len(movement)

    # Unique devices
    unique_devices = movement["DeviceID"].nunique()

    # Total observed distance
    total_distance = movement["Distance_KM"].sum()

    # Average observed speed
    average_speed = movement["Speed_KMH"].mean()

    # Total clusters
    total_clusters = clusters["Cluster"].nunique()

    # Best silhouette score
    best_silhouette = evaluation["Silhouette_Score"].max()

    st.subheader("GeoPulse Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "GPS Records",
        f"{total_records:,}"
    )

    col2.metric(
        "Unique Devices",
        f"{unique_devices:,}"
    )

    col3.metric(
        "Total Distance",
        f"{total_distance:,.2f} km"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Average Speed",
        f"{average_speed:.2f} km/h"
        if pd.notna(average_speed) else "N/A"
    )

    col5.metric(
        "Clusters",
        total_clusters
    )

    col6.metric(
        "Best Silhouette Score",
        f"{best_silhouette:.4f}"
        if pd.notna(best_silhouette) else "N/A"
    )