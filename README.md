# GeoPulse
Hyper-Local Retail Mobility Analytics using Python, Snowflake, Apache Sedona, PySpark, dbt and Kepler.gl to analyze foot traffic, store catchment areas and retail location opportunities.
## License

GeoPulse is licensed under the GNU General Public License v3.0 (GPL-3.0).

You may redistribute and modify this software under the terms of the GNU GPL version 3, or (at your option) any later version.

This software is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**, including the implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the [`LICENSE`](LICENSE) file for the complete license terms.

**Copyright:** Copyright (C) 2026 [COPYRIGHT HOLDER TO BE CONFIRMED]

For the full license text, see the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

:::writing{variant="document" id="73104"}
## Running the GeoPulse Dashboard

### Requirements

- Python 3.10 or compatible version
- Git
- Internet connection for initial dependency installation

### Installation

Clone the repository:

```bash
git clone https://github.com/abhimanyu-123456/GeoPulse.git
cd GeoPulse
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the Python source path on Windows:

```powershell
$env:PYTHONPATH = "src"
```

### Run the dashboard

```bash
streamlit run dashboard/app.py
```

Open the local URL displayed by Streamlit, normally:

http://localhost:8501

### Run tests

```bash
python -m pytest tests -v
```

### Data and Limitations

GeoPulse uses synthetic GPS observations for educational and analytical demonstration.

Its calculated movement metrics and machine-learning clusters are estimates and analytical groupings, not verified real-world transportation classifications.

The project is not designed for tracking real individuals.

### License

GeoPulse is distributed under the GNU General Public License v3.0.

See the LICENSE file for the complete license terms.
:::

## Live Dashboard

GeoPulse is deployed using Streamlit Community Cloud.

**Live Application:** https://geopulse-dashboard-abhi.streamlit.app

The interactive dashboard provides:
- GPS analytics KPIs
- Device-level movement summaries
- Movement category analysis
- Device and cluster filters
- Interactive visualizations
- Clustering evaluation

**Note:** GeoPulse uses synthetic GPS data and is intended for educational and analytical demonstration.


## Live Dashboard

GeoPulse includes an interactive dashboard developed using Streamlit and Plotly.

The dashboard provides:

- GPS dataset overview and key performance indicators.
- Device-level movement analytics.
- Cluster distribution visualizations.
- Average speed and distance analysis.
- Interactive filters for cluster, device, movement category, and date range.
- Machine-learning clustering evaluation metrics.

### Deployment

The dashboard is deployed using Streamlit Community Cloud.

**Live Application:** https://geopulse-dashboard-abhi.streamlit.app/

### Data Limitations

This project uses synthetic GPS observations for educational and analytical purposes. The clustering results represent mathematical groupings and should not be interpreted as verified real-world transportation categories or individual behaviour.

## Project Workflow

The GeoPulse system follows a structured data analytics workflow:

1. GPS data preparation and preprocessing.
2. Movement distance and speed calculation.
3. Movement pattern classification.
4. Device-level feature extraction.
5. Machine-learning clustering.
6. Cluster interpretation and model evaluation.
7. Analytics report generation.
8. Interactive dashboard development.
9. Dashboard deployment using Streamlit Community Cloud.

## Future Improvements

Potential future enhancements include:

- Additional clustering algorithms.
- Improved model comparison and evaluation.
- More interactive data visualizations.
- Enhanced dashboard reporting.
- Better handling of missing and invalid observations.

## Project Conclusion

GeoPulse demonstrates how Python, data analytics, and machine learning can be combined to analyze synthetic GPS observations and present meaningful analytical summaries through an interactive web dashboard.