# Pacos NetInsight

Pacos NetInsight is an AI-driven network anomaly detection dashboard built with Python and Streamlit. It analyzes network log CSV files, detects suspicious packet flows, assigns risk levels, and helps security analysts spot abnormal behavior quickly.

## Features
- Network log ingestion from CSV files
- Isolation Forest anomaly detection
- Traffic type classification and risk scoring
- Streamlit dashboard with summary metrics, time series, and suspicious activity view
- Optional traffic forecasting using Prophet
- Sample log generation for testing and demo purposes

## Installation

```bash
git clone https://github.com/KLIIRTY/PacosNetInsight.git
cd PacosNetInsight
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running locally

1. Generate sample data (optional):

```bash
python src/generate_logs.py
```

2. Start the Streamlit app:

```bash
streamlit run src/app.py
```

3. Run the CLI analyzer:

```bash
python src/main.py
```

## Project structure

```
PacosNetInsight/
├─ data/
│  └─ network_log.csv
├─ src/
│  ├─ app.py
│  ├─ features.py
│  ├─ generate_logs.py
│  ├─ main.py
│  ├─ model.py
│  ├─ net_parser.py
│  ├─ prediction.py
│  └─ __init__.py
├─ requirements.txt
└─ README.md
```

## Tests

```bash
pytest
```
