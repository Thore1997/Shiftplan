import pandas as pd
import io


def get_employee_df(file_path="Mitarbeiter.csv"):
    """
    Reads the employee CSV file, cleans formatting, and sets the ID as the index.
    """
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Remove quotes to prevent formatting issues
    content = content.replace('"', '')

    # Load into DataFrame
    df = pd.read_csv(io.StringIO(content), sep=';')

    # Strip whitespace from column headers
    df.columns = df.columns.str.strip()

    if 'ID' in df.columns:
        df.set_index('ID', inplace=True)
        # IMPORTANT: Convert index to string to prevent type errors in PuLP
        df.index = df.index.astype(str)

    return df