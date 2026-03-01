# src/net_parser.py
import pandas as pd

def load_csv(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    # Remove empty columns (from trailing tabs)
    df = df.loc[:, df.columns.notnull()]
    # Normalize column names: lowercase, strip spaces, replace spaces with underscore
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    return df