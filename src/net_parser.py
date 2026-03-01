import pandas as pd

def load_csv(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig', sep=',')
    # Remove empty columns (e.g., trailing tabs)
    df = df.loc[:, df.columns.notnull()]
    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df