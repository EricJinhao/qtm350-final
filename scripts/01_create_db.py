# scripts/01_create_db.py
import sqlite3
import pandas as pd
from pathlib import Path


def main():
    # 1. make sure data folder exists (inside current repo)
    db_path = Path("data/wdi.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # 2. connect to sqlite
    conn = sqlite3.connect(db_path)

    # 3. read your raw CSVs (already in data/raw/)
    raw = pd.read_csv("data/raw/wdi_pophealth_data.csv")
    meta = pd.read_csv("data/raw/wdi_pophealth_metadata.csv")

    # 4. write them into sqlite as raw tables
    raw.to_sql("raw_wdi_data", conn, if_exists="replace", index=False)
    meta.to_sql("raw_wdi_metadata", conn, if_exists="replace", index=False)

    print("Tables raw_wdi_data and raw_wdi_metadata created in data/wdi.db")
    conn.close()


if __name__ == "__main__":
    main()

