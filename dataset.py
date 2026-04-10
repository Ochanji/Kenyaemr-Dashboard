"""
dataset.py
----------
Database connection and DataFrame extraction for the KenyaEMR Dashboard.

Connects to the kenyaemr_etl MySQL database using credentials stored in a
.env file, then loads each programme dataset into a Pandas DataFrame that
is imported by app.py.

Required environment variables (.env):
    DB_USER      - MySQL username
    DB_PASSWORD  - MySQL password
    DB_HOST      - MySQL host (default: 127.0.0.1)
    DB_PORT      - MySQL port (default: 3306)
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load credentials from .env (never commit real credentials to version control)
# ---------------------------------------------------------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = "kenyaemr_etl"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)


# ---------------------------------------------------------------------------
# Helper: bootstrap the etl_provider lookup table
# ---------------------------------------------------------------------------
def _bootstrap_provider_table() -> None:
    """Create (or recreate) the etl_provider lookup table from the SQL file."""
    sql_file = os.path.join("sql_queries", "etl_provider table.sql")
    with open(sql_file, "r") as f:
        statements = f.read().split(";\n")

    with engine.begin() as conn:
        conn.execute(text("USE kenyaemr_etl"))
        conn.execute(text("DROP TABLE IF EXISTS etl_provider"))
        conn.execute(
            text(
                "CREATE TABLE etl_provider "
                "(creator_id VARCHAR(50), provider VARCHAR(50))"
            )
        )
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                conn.execute(text(stmt))


_bootstrap_provider_table()


# ---------------------------------------------------------------------------
# Helper: load a DataFrame from a SQL file
# ---------------------------------------------------------------------------
def _load_sql(path: str) -> pd.DataFrame:
    """Execute all statements in the given SQL file and return the last result."""
    with open(path, "r") as f:
        statements = f.read().split(";\n")

    df = pd.DataFrame()
    with engine.connect() as conn:
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                df = pd.read_sql(text(stmt), conn)
    return df


# ---------------------------------------------------------------------------
# Age-band configuration (reused across multiple datasets)
# ---------------------------------------------------------------------------
AGE_BINS = [0, 14, 19, 24, 29, 34, 39, 44, 49, 1000]
AGE_LABELS = ["<15", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50+"]


# ---------------------------------------------------------------------------
# Load all datasets
# ---------------------------------------------------------------------------

# Overview - programme-wide KPI summary
df_overview = _load_sql(os.path.join("sql_queries", "overview.sql"))

# HIV Testing Services (HTS)
df_hts = _load_sql(os.path.join("sql_queries", "HTS.sql"))
df_hts["AgeGroup"] = pd.cut(
    df_hts["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True
)
df_hts.drop_duplicates(
    subset=["First Name", "Middle Name", "Last Name", "Age", "Gender"],
    keep="first",
    inplace=True,
)

# Prevention Services - PrEP (merge new initiations and current clients)
_prep_new = _load_sql(os.path.join("sql_queries", "PREP.sql"))
_prep_ct = _load_sql(os.path.join("sql_queries", "PREP ct.sql"))
df_prep = pd.merge(left=_prep_new, right=_prep_ct, how="left", on="patient_id")

# HIV Care and Treatment (CT)
df_ct = _load_sql(os.path.join("sql_queries", "ct.sql"))
df_ct.drop_duplicates(
    subset=["First Name", "Middle Name", "Last Name", "Age", "Gender"],
    keep="first",
    inplace=True,
)
df_ct["AgeGroup"] = pd.cut(
    df_ct["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True
)

# KP Prevention Services (KP_PREV / GBV)
df_prevention = _load_sql(os.path.join("sql_queries", "prevention.sql"))
