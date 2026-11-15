
"""
GeoPulse - GPS-Based Movement Analytics System

Interactive analytics dashboard using Streamlit.
"""

import streamlit as st

# Import dashboard modules consistently.
# Streamlit adds the app.py directory to Python's import path.
from utils.data_loader import (
    load_dashboard_data,
    DataLoadError,
)

from components.metrics import display_metrics
from components.charts import display_charts
from components.filters import apply_filters


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="GeoPulse Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# MAIN APPLICATION
# ==================================================

def main():

    st.title("🌍 GeoPulse")

    st.subheader(
        "GPS-Based Movement Analytics System"
    )

    st.markdown(
        """
        GeoPulse is a Python-based movement analytics
        demonstration using synthetic GPS observations
        around Bhopal, India.

        It analyzes movement metrics, classifies observed
        movement patterns, and applies machine-learning
        clustering to device-level summaries.
        """
    )

    st.divider()

    # ----------------------------------------------
    # LOAD DATA
    # ----------------------------------------------

    try:

        data = load_dashboard_data()

    except DataLoadError as error:

        st.error(f"Dashboard data error: {error}")

        st.info(
            "Check whether the required processed CSV "
            "files exist and contain the expected columns."
        )

        st.stop()

    except (
        OSError,
        ValueError,
        KeyError,
        ImportError,
    ) as error:

        st.error(f"Unexpected dashboard error: {error}")

        st.stop()

    st.success(
        "All dashboard datasets loaded successfully."
    )

    # ----------------------------------------------
    # DATA FILTERS
    # ----------------------------------------------

    filtered_data = apply_filters(data)

    st.divider()

    # ----------------------------------------------
    # KPI METRICS
    # ----------------------------------------------

    st.header("Project Overview")

    display_metrics(filtered_data)

    st.divider()

    # ----------------------------------------------
    # INTERACTIVE CHARTS
    # ----------------------------------------------

    st.header("Movement Analytics")

    display_charts(filtered_data)

    st.divider()

    # ----------------------------------------------
    # DEVICE SUMMARY TABLE
    # ----------------------------------------------

    st.header("Device-Level Analytics")

    device_data = filtered_data["device_clusters"]

    if device_data.empty:

        st.warning(
            "No device records match the selected filters."
        )

    else:

        st.dataframe(
            device_data,
            use_container_width=True,
            hide_index=True,
        )

    # ----------------------------------------------
    # DATASET INFORMATION
    # ----------------------------------------------

    st.header("Dataset Information")

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown(
            """
            **Project Area:** Bhopal, India

            **Data Type:** Synthetic GPS observations

            **Original Dataset:** 10,000 GPS records

            **Original Devices:** 1,994
            """
        )

    with info_col2:

        st.markdown(
            """
            **Technology Stack**

            - Python
            - Pandas
            - NumPy
            - Scikit-learn
            - Streamlit
            - Plotly
            """
        )

    # ----------------------------------------------
    # PROJECT LIMITATIONS
    # ----------------------------------------------

    st.header("Data Limitations")

    st.warning(
        """
        GeoPulse uses synthetic GPS data and is intended
        for educational and analytical demonstration.

        Calculated distances and speeds are estimates
        between recorded observations.

        Long observation intervals can make average
        speed estimates misleading.

        Clusters are mathematical groupings and should
        not automatically be interpreted as real
        transportation categories or actual behaviour.

        This dashboard is not designed for tracking
        real individuals.
        """
    )

    # ----------------------------------------------
    # FOOTER
    # ----------------------------------------------

    st.divider()

    st.caption(
        "GeoPulse | GPS-Based Movement Analytics System"
    )

    st.caption(
        "Educational Data Analytics Project | GPL-3.0"
    )


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
