# src/net_parser.py
import pandas as pd

def load_csv(file_path):
    """Load a network log CSV for analysis."""
    df = pd.read_csv(file_path)
    return df