# src/net_parser.py
import pandas as pd

def load_csv(uploaded_file):
    """Load a network log CSV for analysis."""
    uploaded_file.seek(0)  # <-- reset pointer
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig', sep=',')
    # Remove completely empty columns
    df = df.loc[:, df.columns.notnull()]
    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df