#### upload_to_mongodb.py

import os
import pandas as pd
from pymongo import MongoClient
import json


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
    elif ext == '.json':
        with open(filename, 'r') as f:
            data = json.load(f)
        if isinstance(data, list):
            dataframes = {'data': pd.DataFrame(data)}
        elif isinstance(data, dict):
            dataframes = {k: pd.DataFrame(v) if isinstance(v, list) else pd.DataFrame([v]) for k, v in data.items()}
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
    return dataframes


def upload_to_mongodb(filename, mongo_url, db_name):
    dataframes = read_data_from_file(filename)
    client = MongoClient(mongo_url)
    db = client[db_name]

    for collection_name, df in dataframes.items():
        records = df.to_dict('records')
        db[collection_name].insert_many(records)
        print(f"Transferred collection: {collection_name}")

    client.close()