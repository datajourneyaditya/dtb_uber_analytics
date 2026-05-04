# utils/databricks_conn.py
import os
import streamlit as st
from databricks import sql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_connection():
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN"),
        catalog="dbt_uber_analytics_catalog",
        schema="dbt_asawant_marts"
    )


@st.cache_data(ttl=300)
def run_query(_conn, query: str) -> pd.DataFrame:
    with _conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
    return pd.DataFrame(rows, columns=cols)