# src/net_parser.py
import pandas as pd
import io

def load_csv(uploaded_file):
    """
    Load a network log CSV for analysis and normalize columns.
    Handles:
        - BOM / UTF-8-sig
        - Extra spaces in headers
        - Trailing commas / empty columns
        - Uploaded file-like objects
    """
    try:
        # Reset file pointer if re-uploaded
        if hasattr(uploaded_file, 'seek'):
            uploaded_file.seek(0)

        # Read CSV (handle UTF-8 BOM, comma separator)
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig', sep=',', engine='python')

        # Remove completely empty columns (e.g., from trailing commas)
        df = df.loc[:, df.columns.notnull()]

        # Normalize column names: lowercase, strip spaces, replace spaces with underscores
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        # Strip leading/trailing spaces in string values
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()

        return df

    except pd.errors.EmptyDataError:
        raise ValueError("Uploaded CSV is empty or invalid.")
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")