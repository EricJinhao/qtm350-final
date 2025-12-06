# scripts/02_clean_wdi.py
import sqlite3
import pandas as pd
from pathlib import Path


def main():
    conn = sqlite3.connect("data/wdi.db")

    # 1. load raw from sqlite
    raw = pd.read_sql_query("SELECT * FROM raw_wdi_data;", conn)

    # 2. pick year columns: names start with 4-digit year, e.g. "1993 [YR1993]"
    year_cols = [c for c in raw.columns if c[:4].isdigit()]
    print("Year columns example:", year_cols[:5])

    # 3. melt wide -> long
    data_long = raw.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=year_cols,
        var_name="year_raw",
        value_name="value",
    )

    # 4. clean column names
    data_long = data_long.rename(
        columns={
            "Country Name": "country_name",
            "Country Code": "country_code",
            "Series Name": "indicator_name",
            "Series Code": "indicator_code",
        }
    )

    # 5. extract numeric year from "1993 [YR1993]" -> 1993
    data_long["year"] = data_long["year_raw"].str.slice(0, 4).astype(int)
    data_long = data_long.drop(columns="year_raw")

    print("Unique country codes:", data_long["country_code"].unique())
    print("Unique indicator codes:", data_long["indicator_code"].unique())
    print("Year range:", data_long["year"].min(), "to", data_long["year"].max())
    print("Non-missing values count:", data_long["value"].notna().sum())

    # 6. filter to our countries / indicators / years
    keep_countries = ["CHN", "IND", "JPN"]
    keep_indicators = ["SP.DYN.LE00.IN", "SH.DYN.MORT", "SP.ADO.TFRT"]

    mask = (
        data_long["country_code"].isin(keep_countries)
        & data_long["indicator_code"].isin(keep_indicators)
        & data_long["year"].between(1993, 2023)
        & data_long["value"].notna()
    )

    clean = data_long.loc[mask].reset_index(drop=True)
    print("Clean shape:", clean.shape)
    print(clean.head())

    # 7. save back to sqlite + CSV
    clean.to_sql("wdi_pophealth_clean", conn, if_exists="replace", index=False)

    Path("data/clean").mkdir(parents=True, exist_ok=True)
    clean.to_csv("data/clean/wdi_pophealth_clean.csv", index=False)

    # (optional) also create a wdi_values table identical to clean
    clean.to_sql("wdi_values", conn, if_exists="replace", index=False)

    conn.close()
    print("Recreated wdi_pophealth_clean and wdi_values + CSV.")


if __name__ == "__main__":
    main()
