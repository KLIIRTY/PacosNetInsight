# src/net_parser.py
import pandas as pd

def load_csv(uploaded_file):
    """
    Load a network log CSV for Streamlit safely.
    Handles uploaded files and normalizes column names.
    """
    # Reset file pointer (important for repeated reads in Streamlit)
    uploaded_file.seek(0)

    # Read CSV
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig', sep=',')

    # Remove completely empty columns (e.g., trailing commas)
    df = df.loc[:, df.columns.notnull()]

    # Strip whitespace and normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Ensure dataframe is not empty
    if df.empty:
        raise ValueError("Uploaded CSV is empty or invalid.")

    return df