# src/net_parser.py
import pandas as pd

def load_csv(uploaded_file):
    """
    Load a network log CSV from a Streamlit file uploader.
    """
    # Ensure the uploaded file is read correctly as CSV
    df = pd.read_csv(uploaded_file)
    
    # Optional: normalize column names to prevent KeyErrors
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    return df