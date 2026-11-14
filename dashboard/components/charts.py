
"""
GeoPulse - Interactive Dashboard Charts
"""

import pandas as pd
import plotly.express as px
import streamlit as st

def display_charts(data):

    profiles = data["cluster_profiles"]
    devices = data["device_clusters"]
    patterns = data["movement_patterns"]
    evaluation = data["clustering_evaluation"]

    st.header("Cluster Analysis")

    # ------------------------------------------------
    # CHART 1: CLUSTER DISTRIBUTION
    # ------------------------------------------------

    st.subheader("1. Cluster Distribution")

    fig1 = px.bar(
        profiles,
        x="Cluster",
        y="Device_Count",
        color="Cluster",
        title="Number of Devices in Each Cluster",
        labels={
            "Device_Count": "Number of Devices",
            "Cluster": "Cluster"
        },
        text="Device_Count"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ------------------------------------------------
    # CHART 2: AVERAGE SPEED
    # ------------------------------------------------

    st.subheader("2. Average Speed by Cluster")

    fig2 = px.bar(
        profiles,
        x="Cluster",
        y="Average_Speed_KMH",
        color="Cluster",
        title="Average Speed by Cluster",
        labels={
            "Average_Speed_KMH": "Average Speed (km/h)"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ------------------------------------------------
    # CHART 3: AVERAGE DISTANCE
    # ------------------------------------------------

    st.subheader("3. Average Distance by Cluster")

    fig3 = px.bar(
        profiles,
        x="Cluster",
        y="Average_Distance_KM",
        color="Cluster",
        title="Average Distance by Cluster",
        labels={
            "Average_Distance_KM": "Average Distance (km)"
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ------------------------------------------------
    # CHART 4: DISTANCE VS SPEED
    # ------------------------------------------------

    st.subheader("4. Distance vs Speed")

    fig4 = px.scatter(
        devices,
        x="Average_Speed_KMH",
        y="Total_Distance_KM",
        color="Cluster",
        hover_data=["DeviceID"],
        title="Device Distance vs Average Speed",
        labels={
            "Average_Speed_KMH": "Average Speed (km/h)",
            "Total_Distance_KM": "Total Observed Distance (km)"
        }
    )

    st.plotly_chart(fig4, use_container_width=True)

    # ------------------------------------------------
    # CHART 5: MOVEMENT CATEGORY DISTRIBUTION
    # ------------------------------------------------

    st.header("Movement Pattern Analysis")

    category_counts = (
        patterns["Speed_Category"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Speed_Category")
        .reset_index(name="Count")
    )

    fig5 = px.pie(
        category_counts,
        names="Speed_Category",
        values="Count",
        title="Movement Category Distribution",
        hole=0.35
    )

    st.plotly_chart(fig5, use_container_width=True)

    # ------------------------------------------------
    # CHART 6: MODEL EVALUATION
    # ------------------------------------------------

    st.header("Model Evaluation")

    fig6 = px.line(
        evaluation,
        x="Number_of_Clusters",
        y="Silhouette_Score",
        markers=True,
        title="Silhouette Score for Different K Values",
        labels={
            "Number_of_Clusters": "Number of Clusters (K)",
            "Silhouette_Score": "Silhouette Score"
        }
    )

    st.plotly_chart(fig6, use_container_width=True)