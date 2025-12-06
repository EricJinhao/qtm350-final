# Codebook: Population Health Convergence Project

This codebook documents the variables used in our analysis dataset (`wdi_values` table in `data/wdi.db` and `data/clean/wdi_pophealth_clean.csv`).

## Core variables

| variable       | type   | description                                                           | units / coding                                        |
|----------------|--------|------------------------------------------------------------------------|-------------------------------------------------------|
| `country_code` | string | ISO 3-letter country code                                             | `CHN` = China, `IND` = India, `JPN` = Japan           |
| `country_name` | string | Country name                                                          | “China”, “India”, “Japan”                             |
| `indicator_code` | string | World Development Indicators (WDI) series code                     | examples below                                        |
| `indicator_name` | string | Human-readable indicator label from WDI                            | examples below                                        |
| `year`         | int    | Calendar year                                                         | 1993–2023                                             |
| `value`        | float  | Indicator value for given country, indicator, and year               | depends on indicator (see table below)                |

## Indicators used

| indicator_code | indicator_name                                        | meaning / interpretation                                                                 | units                                                   |
|----------------|-------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------|
| `SP.DYN.LE00.IN` | Life expectancy at birth, total (years)            | Average number of years a newborn is expected to live if current mortality rates persist | years                                                   |
| `SH.DYN.MORT` | Mortality rate, under-5 (per 1,000 live births)       | Probability that a child born in a given year will die before age 5                      | deaths per 1,000 live births                            |
| `SP.ADO.TFRT` | Adolescent fertility rate (births per 1,000 women 15–19) | Annual number of births to women ages 15–19 per 1,000 women in that age group        | births per 1,000 women aged 15–19                       |

## Database tables

Our SQLite database `data/wdi.db` contains three tables:

- **`countries`**  
  - `country_code` (PK)  
  - `country_name`

- **`indicators`**  
  - `indicator_code` (PK)  
  - `indicator_name`

- **`wdi_values`**  
  - `country_code` (FK → countries.country_code)  
  - `indicator_code` (FK → indicators.indicator_code)  
  - `year`  
  - `value`

Each row of `wdi_values` corresponds to a single country–indicator–year observation.
