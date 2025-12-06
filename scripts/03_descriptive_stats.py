# scripts/03_descriptive_stats.py
import sqlite3
import pandas as pd


def main():
    conn = sqlite3.connect("data/wdi.db")

    stats = pd.read_sql_query(
        """
        SELECT country_code,
               indicator_code,
               MIN(value) AS min_val,
               MAX(value) AS max_val,
               AVG(value) AS avg_val
        FROM wdi_values
        GROUP BY country_code, indicator_code;
        """,
        conn,
    )

    conn.close()
    print(stats)


if __name__ == "__main__":
    main()
