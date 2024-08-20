import os
import pandas as pd
from sqlalchemy import create_engine
import backend.config as cfg
def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()

def read_data_from_file(filename):
    ext = get_file_extension(filename)
    if ext in ['.sqlite', '.db']:
        import sqlite3
        sqlite_conn = sqlite3.connect(filename)
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", sqlite_conn)['name'].tolist()
        dataframes = {table: pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn) for table in tables}
        sqlite_conn.close()
    elif ext == '.csv':
        dataframes = {os.path.basename(filename): pd.read_csv(filename)}
    elif ext in ['.xls', '.xlsx']:
        dataframes = pd.read_excel(filename, sheet_name=None)  # Read all sheets
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    return dataframes

def upload_to_postgresql(filename, pg_url):
    dataframes = read_data_from_file(filename)
    # pg_url = cfg.DATABASE_URL
    pg_engine = create_engine(pg_url)
    for table_name, df in dataframes.items():
        df.to_sql(table_name, pg_engine, if_exists='replace', index=False)
        print(f"Transferred table: {table_name}")
    pg_engine.dispose()

# def main():
#     filename = 'datasets/cars.sqlite'  # Replace with your database file
#     pg_url = 'postgresql+psycopg2://postgres:admin123@localhost:5432/car_inventory'  # Replace with your PostgreSQL details
#
#
#     upload_to_postgresql(dataframes, pg_url)
#
# if __name__ == '__main__':
#     main()

