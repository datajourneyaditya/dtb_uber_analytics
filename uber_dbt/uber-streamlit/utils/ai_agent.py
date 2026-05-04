# utils/ai_agent.py
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = """
Available tables:

dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
  booking_date, vehicle_type, vehicle_category, is_premium,
  payment_method, total_bookings, completed_rides,
  total_revenue_inr, avg_fare_inr, avg_distance_km,
  avg_completion_rate_pct, revenue_per_km, revenue_dod_change_inr

dbt_uber_analytics_catalog.dbt_asawant_marts.mart_driver_scorecard
  vehicle_type, pickup_location, vehicle_category, is_premium,
  total_trips, completed_trips, driver_cancels, avg_driver_rating,
  avg_pickup_time_mins, completion_rate_pct,
  performance_tier, reliability_score

dbt_uber_analytics_catalog.dbt_asawant_marts.mart_cancellation_insights
  booking_date, vehicle_type, pickup_location,
  customer_cancel_reason, customer_cancel_category,
  customer_cancel_is_app_issue, driver_cancel_reason,
  driver_cancel_category, total_cancels,
  avg_wait_mins, rolling_7d_cancels

dbt_uber_analytics_catalog.dbt_asawant_marts.mart_customer_segments
  customer_id, customer_tier, churn_risk, tier_since,
  first_booking_date, last_booking_date, tenure_days,
  total_bookings, completed_rides, lifetime_spend_inr,
  avg_customer_rating, cancel_rate_pct,
  days_since_last_ride, is_dormant

dbt_uber_analytics_catalog.dbt_asawant_snapshots.customer_tier_snapshot
  customer_id, customer_tier, churn_risk,
  dbt_valid_from, dbt_valid_to
  -- dbt_valid_to IS NULL = current active record

dbt_uber_analytics_catalog.dbt_asawant_snapshots.driver_score_snapshot
  vehicle_type, pickup_location, performance_tier,
  reliability_score, dbt_valid_from, dbt_valid_to
  -- dbt_valid_to IS NULL = current active record
"""

SQL_SYSTEM = f"""You are a Databricks SQL expert analyst for an Uber NCR operations team.
Convert natural language questions into valid Databricks SQL SELECT statements.

{SCHEMA}

Rules:
- Always fully qualify: dbt_uber_analytics_catalog.dbt_asawant_marts.<table>
- Snapshots: dbt_uber_analytics_catalog.dbt_asawant_snapshots.<table>
- Never write INSERT, UPDATE, DELETE, DROP or CREATE
- For current SCD2 records: WHERE dbt_valid_to IS NULL
- Use try_cast() instead of cast() for safety
- Output ONLY raw SQL — no markdown, no backticks, no explanation
- Add LIMIT 500 unless the query is a pure aggregate
- Use Databricks SQL syntax only"""

INSIGHT_SYSTEM = """You are a senior data analyst for an Uber NCR operations team.
Given a business question, the SQL executed, and the results:

1. State the single most important insight (1-2 sentences)
2. List 2-3 supporting data points from the results
3. Give one specific actionable recommendation for the ops team

Be concise and business-focused. No technical jargon."""


def _call(system: str, user: str, max_tokens: int = 1024) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user}
        ],
        max_tokens=max_tokens,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()


def generate_sql(question: str) -> str:
    return _call(SQL_SYSTEM, question, max_tokens=512)


def generate_insight(question: str, sql_text: str, df: pd.DataFrame) -> str:
    user = f"""Question: {question}

SQL executed:
{sql_text}

Results ({len(df)} total rows, showing first 20):
{df.head(20).to_markdown(index=False)}"""

    return _call(INSIGHT_SYSTEM, user, max_tokens=400)