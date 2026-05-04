# app.py — complete rewrite with 5-tab navigation
import streamlit as st
from dotenv import load_dotenv
from utils.databricks_conn import get_connection, run_query
from utils.theme import apply_theme

load_dotenv()

st.set_page_config(
    page_title="Uber NCR Analytics",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_theme()

# ── top nav bar ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:16px;
            padding:1rem 0 1.25rem;border-bottom:2px solid #F0F0F0;
            margin-bottom:1.5rem">
    <div style="background:#000;color:#fff;font-size:1.3rem;font-weight:700;
                padding:0.25rem 0.85rem;border-radius:5px;letter-spacing:-0.5px">
        Uber
    </div>
    <div style="font-size:0.8rem;color:#767676;font-weight:500;
                text-transform:uppercase;letter-spacing:0.1em">
        NCR · Operations Analytics · 2024
    </div>
</div>
""", unsafe_allow_html=True)

# ── tab navigation ────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Executive overview",
    "Revenue & time",
    "Vehicles",
    "Drivers",
    "Customers",
    "Payments",
    "AI Insights"
])

conn = get_connection()

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    import plotly.express as px
    import plotly.graph_objects as go
    from utils.theme import apply_plotly_theme

    # ── fetch KPIs ────────────────────────────────────────────────────────
    kpi = run_query(conn, """
        SELECT
            sum(total_bookings)                                     as total_bookings,
            sum(completed_rides)                                    as completed_rides,
            round(100.0 * sum(completed_rides)
                  / nullif(sum(total_bookings),0), 0)               as completion_pct,
            round(sum(total_revenue_inr), 0)                        as total_revenue,
            round(avg(avg_fare_inr), 0)                             as avg_fare,
            round(avg(avg_distance_km), 1)                          as avg_distance
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
    """)

    driver_kpi = run_query(conn, """
        SELECT round(avg(avg_driver_rating), 2) as avg_rating
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_driver_scorecard
    """)

    total_bookings  = int(kpi["total_bookings"].iloc[0] or 0)
    completed_rides = int(kpi["completed_rides"].iloc[0] or 0)
    completion_pct  = int(kpi["completion_pct"].iloc[0] or 0)
    total_revenue   = float(kpi["total_revenue"].iloc[0] or 0)
    avg_fare        = float(kpi["avg_fare"].iloc[0] or 0)
    avg_distance    = float(kpi["avg_distance"].iloc[0] or 0)
    avg_rating      = float(driver_kpi["avg_rating"].iloc[0] or 0)
    revenue_cr      = total_revenue / 10_000_000

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Total bookings
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                {total_bookings:,}
            </div>
            <div style="font-size:0.8rem;color:#767676">Full year 2024</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Total revenue
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                ₹{revenue_cr:.2f}Cr
            </div>
            <div style="font-size:0.8rem;color:#767676">Completed rides</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Completion rate
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                {completion_pct}%
            </div>
            <div style="font-size:0.8rem;color:#767676">
                {completed_rides:,} completed
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Avg ride value
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                ₹{avg_fare:.0f}
            </div>
            <div style="font-size:0.8rem;color:#767676">Per completed ride</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    k5, k6, _, _ = st.columns(4)
    with k5:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Avg distance
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                {avg_distance} km
            </div>
            <div style="font-size:0.8rem;color:#767676">Per ride</div>
        </div>
        """, unsafe_allow_html=True)

    with k6:
        st.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;border-radius:10px;
                    padding:1.1rem 1.25rem">
            <div style="font-size:0.7rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em">
                Avg driver rating
            </div>
            <div style="font-size:2rem;font-weight:700;color:#000;
                        margin:0.25rem 0 0.1rem;line-height:1">
                {avg_rating}
            </div>
            <div style="font-size:0.8rem;color:#767676">Out of 5.0</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── row 1: booking status donut + revenue by day of week ─────────────
    col1, col2 = st.columns(2)

    with col1:
        status_df = run_query(conn, """
            SELECT
                booking_status_raw,
                count(*) as cnt
            FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
            GROUP BY booking_status_raw
            ORDER BY cnt DESC
        """)

        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">
                Booking status breakdown
            </div>
        """, unsafe_allow_html=True)

        total = status_df["cnt"].sum()
        labels_with_pct = [
            f"{row['booking_status_raw']} {round(row['cnt']/total*100)}%"
            for _, row in status_df.iterrows()
        ]
        fig_donut = go.Figure(go.Pie(
            labels=labels_with_pct,
            values=status_df["cnt"],
            hole=0.55,
            marker_colors=["#2ECC71","#E67E22","#E74C3C","#3498DB","#95A5A6"],
            textinfo="none",
            hovertemplate="%{label}<br>%{value:,}<extra></extra>"
        ))
        fig_donut.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            legend=dict(
                orientation="v",
                x=0, y=1,
                font=dict(size=12, color="#000"),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        dow_df = run_query(conn, """
            SELECT
                dayofweek(booking_date)     as day_of_week,
                sum(total_revenue_inr)      as revenue
            FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
            GROUP BY dayofweek(booking_date)
            ORDER BY day_of_week
        """)

        day_map = {1:"Sun",2:"Mon",3:"Tue",4:"Wed",5:"Thu",6:"Fri",7:"Sat"}
        dow_df["day_name"] = dow_df["day_of_week"].map(day_map)

        # reorder Mon-Sun
        order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        dow_df["day_name"] = dow_df["day_name"].astype(
            "category"
        ).cat.set_categories(order)
        dow_df = dow_df.sort_values("day_name")

        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">
                Revenue by day of week
            </div>
        """, unsafe_allow_html=True)

        colors_dow = [
            "#276EF1" if d not in ["Sat","Sun"] else "#1AC8A1"
            for d in dow_df["day_name"]
        ]

        fig_dow = go.Figure(go.Bar(
            x=dow_df["day_name"],
            y=dow_df["revenue"],
            marker_color=colors_dow,
            hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>"
        ))
        fig_dow.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            xaxis=dict(
                showgrid=False,
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=12)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#F0F0F0",
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11),
                tickprefix="₹",
                tickformat=".2s"
            ),
            showlegend=False,
            bargap=0.3
        )
        st.plotly_chart(fig_dow, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── row 2: rides by hour + cancellation reasons ───────────────────────
# ── rides by hour — pull from staging which has booking_datetime
    hourly_df = run_query(conn, """
        SELECT
            hour(booking_datetime)      as booking_hour,
            count(*)                    as rides
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE booking_datetime IS NOT NULL
        GROUP BY hour(booking_datetime)
        ORDER BY booking_hour
    """)

    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Rides by hour of day (demand pattern)
        </div>
    """, unsafe_allow_html=True)

    fig_hour = go.Figure(go.Scatter(
        x=hourly_df["booking_hour"],
        y=hourly_df["rides"],
        mode="lines+markers",
        line=dict(color="#1AC8A1", width=2.5),
        marker=dict(color="#1AC8A1", size=5),
        fill="tozeroy",
        fillcolor="rgba(26,200,161,0.12)",
        hovertemplate="Hour %{x}:00<br>%{y:,} rides<extra></extra>"
    ))
    fig_hour.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
        xaxis=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12),
            dtick=2
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickformat=","
        ),
        showlegend=False
    )
    st.plotly_chart(fig_hour, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── cancellation reasons side by side ─────────────────────────────────
    cust_cancel = run_query(conn, """
        SELECT
            customer_cancel_reason,
            sum(total_cancels) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_cancellation_insights
        WHERE customer_cancel_reason IS NOT NULL
          AND lower(trim(customer_cancel_reason)) != 'null'
        GROUP BY customer_cancel_reason
        ORDER BY cnt DESC
        LIMIT 5
    """)

    drv_cancel = run_query(conn, """
        SELECT
            driver_cancel_reason,
            sum(total_cancels) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_cancellation_insights
        WHERE driver_cancel_reason IS NOT NULL
          AND lower(trim(driver_cancel_reason)) != 'null'
        GROUP BY driver_cancel_reason
        ORDER BY cnt DESC
        LIMIT 4
    """)

    total_cust_cancel = int(cust_cancel["cnt"].sum())
    total_drv_cancel  = int(drv_cancel["cnt"].sum())

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:1rem">
            Cancellation reasons
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem">
            <div>
                <div style="font-size:0.85rem;font-weight:600;color:#000;
                            margin-bottom:0.75rem">
                    By customer ({total_cust_cancel:,} rides)
                </div>
                {"".join([
                    f'''<div style="display:flex;align-items:center;
                                   gap:10px;margin-bottom:0.6rem">
                        <div style="font-size:0.82rem;color:#333;
                                    min-width:130px;flex-shrink:0">
                            {row["customer_cancel_reason"]}
                        </div>
                        <div style="flex:1;background:#E8E8E5;
                                    border-radius:99px;height:8px;overflow:hidden">
                            <div style="height:100%;border-radius:99px;
                                        background:#276EF1;width:{
                                            min(100, round(row["cnt"]/max(cust_cancel["cnt"])*100))
                                        }%">
                            </div>
                        </div>
                        <div style="font-size:0.82rem;font-weight:600;
                                    color:#000;min-width:42px;text-align:right">
                            {int(row["cnt"]):,}
                        </div>
                    </div>'''
                    for _, row in cust_cancel.iterrows()
                ])}
            </div>
            <div>
                <div style="font-size:0.85rem;font-weight:600;color:#000;
                            margin-bottom:0.75rem">
                    By driver ({total_drv_cancel:,} rides)
                </div>
                {"".join([
                    f'''<div style="display:flex;align-items:center;
                                   gap:10px;margin-bottom:0.6rem">
                        <div style="font-size:0.82rem;color:#333;
                                    min-width:130px;flex-shrink:0">
                            {row["driver_cancel_reason"]}
                        </div>
                        <div style="flex:1;background:#E8E8E5;
                                    border-radius:99px;height:8px;overflow:hidden">
                            <div style="height:100%;border-radius:99px;
                                        background:#E74C3C;width:{
                                            min(100, round(row["cnt"]/max(drv_cancel["cnt"])*100))
                                        }%">
                            </div>
                        </div>
                        <div style="font-size:0.82rem;font-weight:600;
                                    color:#000;min-width:42px;text-align:right">
                            {int(row["cnt"]):,}
                        </div>
                    </div>'''
                    for _, row in drv_cancel.iterrows()
                ])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — REVENUE & TIME
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    import plotly.graph_objects as go
    import pandas as pd

    rev_df = run_query(conn, """
        SELECT
            booking_date,
            vehicle_type,
            payment_method,
            total_bookings,
            completed_rides,
            total_revenue_inr,
            avg_fare_inr,
            avg_completion_rate_pct,
            revenue_per_km
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
        ORDER BY booking_date
    """)

    rev_df["booking_date"] = pd.to_datetime(rev_df["booking_date"])
    rev_df["month"]        = rev_df["booking_date"].dt.to_period("M").astype(str)
    rev_df["month_name"]   = rev_df["booking_date"].dt.strftime("%b %Y")
    rev_df["day_of_week"]  = rev_df["booking_date"].dt.dayofweek  # 0=Mon

    # ── aggregate monthly ─────────────────────────────────────────────────
    monthly = rev_df.groupby("month").agg(
        revenue=("total_revenue_inr", "sum"),
        rides=("completed_rides", "sum")
    ).reset_index().sort_values("month")
    monthly["month_label"] = pd.to_datetime(
        monthly["month"]
    ).dt.strftime("%b")

    # ── aggregate by day of week ──────────────────────────────────────────
    dow = rev_df.groupby("day_of_week").agg(
        revenue=("total_revenue_inr", "sum")
    ).reset_index()
    day_map = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
    dow["day_name"] = dow["day_of_week"].map(day_map)
    dow_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    dow["day_name"] = pd.Categorical(dow["day_name"], categories=dow_order)
    dow = dow.sort_values("day_name")

    # ── compute KPIs ──────────────────────────────────────────────────────
    annual_rev      = rev_df["total_revenue_inr"].sum()
    monthly_avg     = monthly["revenue"].mean()
    peak_month_row  = monthly.loc[monthly["revenue"].idxmax()]
    peak_label      = pd.to_datetime(peak_month_row["month"]).strftime("%b %Y")
    peak_val        = peak_month_row["revenue"]

    weekend_rev = dow[dow["day_name"].isin(["Sat","Sun"])]["revenue"].mean()
    weekday_rev = dow[~dow["day_name"].isin(["Sat","Sun"])]["revenue"].mean()
    weekend_prem = round((weekend_rev - weekday_rev) / weekday_rev * 100)

    def fmt_lakh(v):
        if v >= 1e7:
            return f"₹{v/1e7:.2f}Cr"
        return f"₹{v/1e5:.1f}L"

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)

    for col, title, value, sub in [
        (k1, "ANNUAL REVENUE",   fmt_lakh(annual_rev),    "2024 total"),
        (k2, "MONTHLY AVG",      fmt_lakh(monthly_avg),   "Per month"),
        (k3, "PEAK MONTH",       peak_label,              fmt_lakh(peak_val)),
        (k4, "WEEKEND PREMIUM",  f"+{weekend_prem}%",     "vs weekday avg"),
    ]:
        col.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;
                    border-radius:10px;padding:1.1rem 1.25rem">
            <div style="font-size:0.68rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.4rem">
                {title}
            </div>
            <div style="font-size:1.85rem;font-weight:700;color:#000;
                        line-height:1.1;margin-bottom:0.2rem">
                {value}
            </div>
            <div style="font-size:0.78rem;color:#767676">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── monthly revenue bar chart ─────────────────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Monthly revenue (₹)
        </div>
    """, unsafe_allow_html=True)

    peak_month_str = peak_month_row["month"]
    bar_colors = [
        "#276EF1" if m != peak_month_str else "#FFCD00"
        for m in monthly["month"]
    ]

    fig_monthly = go.Figure(go.Bar(
        x=monthly["month_label"],
        y=monthly["revenue"],
        marker_color=bar_colors,
        hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>"
    ))
    fig_monthly.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickprefix="₹",
            tickformat=".2s",
            zeroline=False
        ),
        showlegend=False,
        bargap=0.35
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── revenue vs ride count dual axis ───────────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Revenue vs ride count by month
        </div>
    """, unsafe_allow_html=True)

    fig_dual = go.Figure()

    fig_dual.add_trace(go.Bar(
        x=monthly["month_label"],
        y=monthly["revenue"],
        name="Revenue (₹)",
        marker_color="#1AC8A1",
        yaxis="y1",
        hovertemplate="%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
    ))

    fig_dual.add_trace(go.Bar(
        x=monthly["month_label"],
        y=monthly["rides"],
        name="Ride count",
        marker_color="#276EF1",
        yaxis="y2",
        hovertemplate="%{x}<br>Rides: %{y:,}<extra></extra>"
    ))

    fig_dual.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        barmode="group",
        bargap=0.25,
        bargroupgap=0.05,
        legend=dict(
            orientation="h",
            x=0, y=1.08,
            font=dict(size=12, color="#000"),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickprefix="₹",
            tickformat=".2s",
            zeroline=False,
            side="left"
        ),
        yaxis2=dict(
            title="",
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickformat=",",
            zeroline=False,
            overlaying="y",
            side="right"
        )
    )
    st.plotly_chart(fig_dual, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── revenue by day of week ────────────────────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Revenue by day of week
        </div>
    """, unsafe_allow_html=True)

    dow_colors = [
        "#1AC8A1" if d in ["Sat","Sun"] else "#888780"
        for d in dow["day_name"]
    ]

    fig_dow = go.Figure(go.Bar(
        x=dow["day_name"],
        y=dow["revenue"],
        marker_color=dow_colors,
        hovertemplate="%{x}<br>₹%{y:,.0f}<extra></extra>"
    ))
    fig_dow.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickprefix="₹",
            tickformat=".2s",
            zeroline=False
        ),
        showlegend=False,
        bargap=0.35
    )
    st.plotly_chart(fig_dow, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── revenue vs ride count dual axis — LINE chart ──────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Revenue vs ride count by month
        </div>
    """, unsafe_allow_html=True)

    fig_dual = go.Figure()

    fig_dual.add_trace(go.Scatter(
        x=monthly["month_label"],
        y=monthly["revenue"],
        name="Revenue (₹)",
        mode="lines+markers",
        line=dict(color="#1AC8A1", width=2.5),
        marker=dict(color="#1AC8A1", size=6),
        yaxis="y1",
        hovertemplate="%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
    ))

    fig_dual.add_trace(go.Scatter(
        x=monthly["month_label"],
        y=monthly["rides"],
        name="Ride count",
        mode="lines+markers",
        line=dict(color="#276EF1", width=2.5),
        marker=dict(color="#276EF1", size=6),
        yaxis="y2",
        hovertemplate="%{x}<br>Rides: %{y:,}<extra></extra>"
    ))

    fig_dual.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            x=0, y=1.08,
            font=dict(size=12, color="#000"),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickprefix="₹",
            tickformat=".2s",
            zeroline=False,
            side="left"
        ),
        yaxis2=dict(
            showgrid=False,
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickformat=",",
            zeroline=False,
            overlaying="y",
            side="right"
        )
    )
    st.plotly_chart(fig_dual, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — VEHICLES
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — VEHICLES
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — VEHICLES
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    import plotly.graph_objects as go
    import pandas as pd

    veh_df = run_query(conn, """
        SELECT
            vehicle_type,
            sum(total_bookings)             as total_bookings,
            sum(completed_rides)            as completed_rides,
            sum(total_revenue_inr)          as total_revenue_inr,
            round(avg(avg_fare_inr), 0)     as avg_fare_inr,
            round(avg(avg_distance_km), 1)  as avg_distance_km,
            round(avg(avg_completion_rate_pct), 1) as completion_rate_pct,
            round(avg(revenue_per_km), 2)   as revenue_per_km
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
        GROUP BY vehicle_type
        ORDER BY total_revenue_inr DESC
    """)

    vtat_df = run_query(conn, """
        SELECT
            vehicle_type,
            round(avg(driver_arrival_mins), 1) as avg_vtat,
            round(avg(trip_duration_mins), 1)  as avg_ctat
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE driver_arrival_mins IS NOT NULL
          AND trip_duration_mins  IS NOT NULL
        GROUP BY vehicle_type
    """)

    incomplete_df = run_query(conn, """
        SELECT
            incomplete_reason,
            count(*) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE is_incomplete = true
          AND incomplete_reason IS NOT NULL
          AND lower(trim(incomplete_reason)) != 'null'
        GROUP BY incomplete_reason
        ORDER BY cnt DESC
    """)

    # merge vtat into veh_df
    veh_df = veh_df.merge(vtat_df, on="vehicle_type", how="left")

    top_vehicle     = veh_df.iloc[0]["vehicle_type"]
    top_revenue     = veh_df.iloc[0]["total_revenue_inr"]
    avg_vtat_all    = veh_df["avg_vtat"].mean()
    avg_ctat_all    = veh_df["avg_ctat"].mean()
    num_types       = len(veh_df)

    def fmt_cr(v):
        return f"₹{v/1e7:.2f}Cr"

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)

    for col, title, value, sub in [
        (k1, "VEHICLE TYPES",  str(num_types),           "Active categories"),
        (k2, "TOP VEHICLE",    top_vehicle,               fmt_cr(top_revenue) + " revenue"),
        (k3, "AVG VTAT",       f"{avg_vtat_all:.1f} min", "All vehicle types"),
        (k4, "AVG CTAT",       f"{avg_ctat_all:.1f} min", "All vehicle types"),
    ]:
        col.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;
                    border-radius:10px;padding:1.1rem 1.25rem">
            <div style="font-size:0.68rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.4rem">
                {title}
            </div>
            <div style="font-size:1.85rem;font-weight:700;color:#000;
                        line-height:1.1;margin-bottom:0.2rem">
                {value}
            </div>
            <div style="font-size:0.78rem;color:#767676">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── revenue donut + ride count bar ────────────────────────────────────
    VEHICLE_COLORS = [
        "#1AC8A1","#276EF1","#7B61FF","#E67E22",
        "#E91E8C","#D4A017","#888780"
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">
                Revenue by vehicle type
            </div>
        """, unsafe_allow_html=True)

        fig_donut = go.Figure(go.Pie(
            labels=veh_df["vehicle_type"],
            values=veh_df["total_revenue_inr"],
            hole=0.52,
            marker_colors=VEHICLE_COLORS[:len(veh_df)],
            textinfo="none",
            hovertemplate="%{label}<br>₹%{value:,.0f}<extra></extra>"
        ))
        fig_donut.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(
                orientation="h",
                x=0, y=1.12,
                font=dict(size=11, color="#000"),
                bgcolor="rgba(0,0,0,0)",
                itemsizing="constant"
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">
                Ride count by vehicle type
            </div>
        """, unsafe_allow_html=True)

        veh_sorted = veh_df.sort_values("completed_rides", ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=veh_sorted["completed_rides"],
            y=veh_sorted["vehicle_type"],
            orientation="h",
            marker_color=VEHICLE_COLORS[:len(veh_sorted)][::-1],
            hovertemplate="%{y}<br>%{x:,} rides<extra></extra>"
        ))
        fig_bar.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis=dict(
                showgrid=True,
                gridcolor="#F0F0F0",
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11),
                tickformat=","
            ),
            yaxis=dict(
                showgrid=False,
                linecolor="#E6E6E6",
                tickfont=dict(color="#333", size=12)
            ),
            showlegend=False,
            bargap=0.25
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


# ── vehicle metrics comparison table ──────────────────────────────────
    table_rows = ""
    for _, row in veh_df.iterrows():
        vtat  = f"{row['avg_vtat']:.1f} min" if row['avg_vtat']  is not None else "—"
        ctat  = f"{row['avg_ctat']:.1f} min" if row['avg_ctat']  is not None else "—"
        name  = str(row['vehicle_type'])
        rides = f"{int(row['completed_rides']):,}"
        rev   = fmt_cr(row['total_revenue_inr'])
        fare  = f"₹{int(row['avg_fare_inr']):,}"
        table_rows += (
            '<tr style="border-bottom:1px solid #F0F0F0">'
            '<td style="padding:0.65rem 0.75rem;font-weight:500;color:#000">' + name  + '</td>'
            '<td style="padding:0.65rem 0.75rem;text-align:right;color:#333">' + rides + '</td>'
            '<td style="padding:0.65rem 0.75rem;text-align:right;color:#333">' + rev   + '</td>'
            '<td style="padding:0.65rem 0.75rem;text-align:right;color:#333">' + fare  + '</td>'
            '<td style="padding:0.65rem 0.75rem;text-align:right;color:#333">' + vtat  + '</td>'
            '<td style="padding:0.65rem 0.75rem;text-align:right;color:#333">' + ctat  + '</td>'
            '</tr>'
        )

    table_html = """
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:1rem">Vehicle metrics comparison</div>
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem">
            <thead>
                <tr style="border-bottom:1.5px solid #E8E8E5">
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Vehicle</th>
                    <th style="text-align:right;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Rides</th>
                    <th style="text-align:right;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Revenue</th>
                    <th style="text-align:right;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Avg fare</th>
                    <th style="text-align:right;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Avg VTAT</th>
                    <th style="text-align:right;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Avg CTAT</th>
                </tr>
            </thead>
            <tbody>ROWS_PLACEHOLDER</tbody>
        </table>
    </div>
    """.replace("ROWS_PLACEHOLDER", table_rows)

    st.markdown(table_html, unsafe_allow_html=True)
    # ── incomplete ride reasons ────────────────────────────────────────────
    incomplete_df = run_query(conn, """
        SELECT
            case
                when lower(trim(incomplete_ride_reason)) like '%vehicle%'
                  or lower(trim(incomplete_ride_reason)) like '%breakdown%'
                  or lower(trim(incomplete_ride_reason)) like '%car%'
                then 'Vehicle breakdown'
                when lower(trim(incomplete_ride_reason)) like '%customer%'
                  or lower(trim(incomplete_ride_reason)) like '%demand%'
                  or lower(trim(incomplete_ride_reason)) like '%request%'
                  or lower(trim(incomplete_ride_reason)) like '%cancel%'
                then 'Customer demand'
                when incomplete_ride_reason is null
                  or lower(trim(incomplete_ride_reason)) = 'null'
                  or lower(trim(incomplete_ride_reason)) = ''
                then null
                else 'Other issue'
            end as reason_group,
            count(*) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE is_incomplete = true
        GROUP BY 1
        HAVING reason_group IS NOT NULL
        ORDER BY cnt DESC
    """)

    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Incomplete ride reasons
        </div>
    """, unsafe_allow_html=True)

    if not incomplete_df.empty and len(incomplete_df) > 1:
        total_incomplete = incomplete_df["cnt"].sum()
        labels_pct = [
            f"{row['reason_group']} {round(row['cnt']/total_incomplete*100)}%"
            for _, row in incomplete_df.iterrows()
        ]

        fig_incomplete = go.Figure(go.Pie(
            labels=labels_pct,
            values=incomplete_df["cnt"],
            hole=0,
            marker_colors=["#E74C3C", "#E67E22", "#888780"],
            textinfo="none",
            hovertemplate="%{label}<br>%{value:,}<extra></extra>"
        ))
        fig_incomplete.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(
                orientation="h",
                x=0, y=1.12,
                font=dict(size=11, color="#000"),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_incomplete, use_container_width=True)

    else:
        # fallback — show raw value distribution if grouping yields one bucket
        incomplete_raw = run_query(conn, """
            SELECT
                coalesce(nullif(trim(incomplete_reason), ''), 'Not specified') as reason,
                count(*) as cnt
            FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
            WHERE is_incomplete = true
            GROUP BY 1
            ORDER BY cnt DESC
        """)

        total = incomplete_raw["cnt"].sum()
        labels_pct = [
            f"{row['reason']} {round(row['cnt']/total*100)}%"
            for _, row in incomplete_raw.iterrows()
        ]

        fig_incomplete = go.Figure(go.Pie(
            labels=labels_pct,
            values=incomplete_raw["cnt"],
            hole=0,
            marker_colors=["#E74C3C", "#E67E22", "#888780", "#276EF1", "#1AC8A1"],
            textinfo="none",
            hovertemplate="%{label}<br>%{value:,}<extra></extra>"
        ))
        fig_incomplete.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(
                orientation="h",
                x=0, y=1.12,
                font=dict(size=11, color="#000"),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_incomplete, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — DRIVERS
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    import plotly.graph_objects as go
    import pandas as pd

    drv_df = run_query(conn, """
        SELECT
            vehicle_type,
            round(avg(avg_driver_rating), 2)    as avg_driver_rating,
            round(avg(avg_pickup_time_mins), 1) as avg_vtat,
            round(avg(completion_rate_pct), 1)  as completion_rate_pct,
            sum(driver_cancels)                 as driver_cancels,
            sum(total_trips)                    as total_trips
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_driver_scorecard
        GROUP BY vehicle_type
        ORDER BY avg_driver_rating DESC
    """)

    vtat_ctat_df = run_query(conn, """
        SELECT
            vehicle_type,
            round(avg(driver_arrival_mins), 1)  as avg_vtat,
            round(avg(trip_duration_mins), 1)   as avg_ctat,
            round(avg(driver_rating), 2)        as avg_driver_rating,
            round(avg(customer_rating), 2)      as avg_customer_rating
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE driver_arrival_mins IS NOT NULL
          AND trip_duration_mins  IS NOT NULL
        GROUP BY vehicle_type
        ORDER BY vehicle_type
    """)

    drv_cancel_df = run_query(conn, """
        SELECT
            driver_cancel_reason,
            sum(total_cancels) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_cancellation_insights
        WHERE driver_cancel_reason IS NOT NULL
          AND lower(trim(driver_cancel_reason)) != 'null'
        GROUP BY driver_cancel_reason
        ORDER BY cnt DESC
        LIMIT 4
    """)

    incomplete_drv_df = run_query(conn, """
        SELECT
            case
                when lower(trim(incomplete_ride_reason)) like '%customer%'
                  or lower(trim(incomplete_ride_reason)) like '%demand%'
                then 'Customer demand'
                when lower(trim(incomplete_ride_reason)) like '%vehicle%'
                  or lower(trim(incomplete_ride_reason)) like '%breakdown%'
                then 'Vehicle breakdown'
                when incomplete_ride_reason is null
                  or lower(trim(incomplete_ride_reason)) = 'null'
                then null
                else 'Other issue'
            end as reason_group,
            count(*) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE is_incomplete = true
        GROUP BY 1
        HAVING reason_group IS NOT NULL
        ORDER BY cnt DESC
    """)

    avg_rating      = vtat_ctat_df["avg_driver_rating"].mean()
    total_drv_cancel = int(drv_cancel_df["cnt"].sum())
    total_trips     = int(drv_df["total_trips"].sum())
    cancel_pct      = round(total_drv_cancel / total_trips * 100) if total_trips else 0
    avg_vtat        = vtat_ctat_df["avg_vtat"].mean()
    avg_ctat        = vtat_ctat_df["avg_ctat"].mean()

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    for col, title, value, sub in [
        (k1, "AVG DRIVER RATING",    f"{avg_rating:.2f}",           "Out of 5.0"),
        (k2, "DRIVER CANCELLATIONS", f"{total_drv_cancel:,}",       f"{cancel_pct}% of bookings"),
        (k3, "AVG VTAT",             f"{avg_vtat:.1f} min",         "Vehicle arrival time"),
        (k4, "AVG CTAT",             f"{avg_ctat:.1f} min",         "Customer arrival time"),
    ]:
        col.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;
                    border-radius:10px;padding:1.1rem 1.25rem">
            <div style="font-size:0.68rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.4rem">{title}</div>
            <div style="font-size:1.85rem;font-weight:700;color:#000;
                        line-height:1.1;margin-bottom:0.2rem">{value}</div>
            <div style="font-size:0.78rem;color:#767676">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── driver cancellation reasons + driver vs customer ratings ──────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">Driver cancellation reasons</div>
        """, unsafe_allow_html=True)

        drv_cancel_sorted = drv_cancel_df.sort_values("cnt", ascending=True)
        fig_cancel = go.Figure(go.Bar(
            x=drv_cancel_sorted["cnt"],
            y=drv_cancel_sorted["driver_cancel_reason"],
            orientation="h",
            marker_color="#E74C3C",
            hovertemplate="%{y}<br>%{x:,}<extra></extra>"
        ))
        fig_cancel.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                showgrid=True, gridcolor="#F0F0F0",
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11),
                tickformat=","
            ),
            yaxis=dict(
                showgrid=False,
                linecolor="#E6E6E6",
                tickfont=dict(color="#333", size=12)
            ),
            showlegend=False,
            bargap=0.3
        )
        st.plotly_chart(fig_cancel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">Driver vs customer ratings</div>
        """, unsafe_allow_html=True)

        fig_ratings = go.Figure()
        fig_ratings.add_trace(go.Bar(
            name="Driver rating",
            x=vtat_ctat_df["vehicle_type"],
            y=vtat_ctat_df["avg_driver_rating"],
            marker_color="#276EF1",
            hovertemplate="%{x}<br>Driver: %{y:.2f}<extra></extra>"
        ))
        fig_ratings.add_trace(go.Bar(
            name="Customer rating",
            x=vtat_ctat_df["vehicle_type"],
            y=vtat_ctat_df["avg_customer_rating"],
            marker_color="#1AC8A1",
            hovertemplate="%{x}<br>Customer: %{y:.2f}<extra></extra>"
        ))
        fig_ratings.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            barmode="group",
            bargap=0.25,
            bargroupgap=0.05,
            legend=dict(
                orientation="h", x=0, y=1.1,
                font=dict(size=11, color="#000"),
                bgcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(
                showgrid=False, linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11)
            ),
            yaxis=dict(
                showgrid=True, gridcolor="#F0F0F0",
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11),
                range=[4.0, 4.6]
            )
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── arrival time performance VTAT vs CTAT ─────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">
            Arrival time performance (VTAT vs CTAT by vehicle)
        </div>
    """, unsafe_allow_html=True)

    fig_vtat = go.Figure()
    fig_vtat.add_trace(go.Bar(
        name="VTAT (vehicle arrival)",
        x=vtat_ctat_df["vehicle_type"],
        y=vtat_ctat_df["avg_vtat"],
        marker_color="#276EF1",
        hovertemplate="%{x}<br>VTAT: %{y:.1f} min<extra></extra>"
    ))
    fig_vtat.add_trace(go.Bar(
        name="CTAT (customer arrival)",
        x=vtat_ctat_df["vehicle_type"],
        y=vtat_ctat_df["avg_ctat"],
        marker_color="#1AC8A1",
        hovertemplate="%{x}<br>CTAT: %{y:.1f} min<extra></extra>"
    ))
    fig_vtat.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        barmode="group",
        bargap=0.25,
        bargroupgap=0.05,
        legend=dict(
            orientation="h", x=0, y=1.1,
            font=dict(size=11, color="#000"),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False, linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            ticksuffix=" min"
        )
    )
    st.plotly_chart(fig_vtat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── service quality overview ───────────────────────────────────────────
    max_drv   = int(drv_cancel_df["cnt"].max()) if not drv_cancel_df.empty else 1
    max_inc   = int(incomplete_drv_df["cnt"].max()) if not incomplete_drv_df.empty else 1

    drv_rows = ""
    for _, row in drv_cancel_df.iterrows():
        pct = round(row["cnt"] / max_drv * 100)
        drv_rows += (
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem">'
            '<div style="font-size:0.82rem;color:#333;min-width:110px;flex-shrink:0">'
            + str(row["driver_cancel_reason"]) +
            '</div>'
            '<div style="flex:1;background:#E8E8E5;border-radius:99px;height:8px;overflow:hidden">'
            '<div style="height:100%;border-radius:99px;background:#E74C3C;width:' + str(pct) + '%"></div>'
            '</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#000;min-width:42px;text-align:right">'
            + f"{int(row['cnt']):,}" +
            '</div>'
            '</div>'
        )

    inc_rows = ""
    for _, row in incomplete_drv_df.iterrows():
        pct = round(row["cnt"] / max_inc * 100)
        inc_rows += (
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:0.55rem">'
            '<div style="font-size:0.82rem;color:#333;min-width:110px;flex-shrink:0">'
            + str(row["reason_group"]) +
            '</div>'
            '<div style="flex:1;background:#E8E8E5;border-radius:99px;height:8px;overflow:hidden">'
            '<div style="height:100%;border-radius:99px;background:#E67E22;width:' + str(pct) + '%"></div>'
            '</div>'
            '<div style="font-size:0.82rem;font-weight:600;color:#000;min-width:42px;text-align:right">'
            + f"{int(row['cnt']):,}" +
            '</div>'
            '</div>'
        )

    quality_html = """
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:1rem">Service quality overview</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem">
            <div>
                <div style="font-size:0.85rem;font-weight:600;color:#000;
                            margin-bottom:0.75rem">Driver cancellation breakdown</div>
                DRV_ROWS
            </div>
            <div>
                <div style="font-size:0.85rem;font-weight:600;color:#000;
                            margin-bottom:0.75rem">Incomplete ride causes</div>
                INC_ROWS
            </div>
        </div>
    </div>
    """.replace("DRV_ROWS", drv_rows).replace("INC_ROWS", inc_rows)

    st.markdown(quality_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — CUSTOMERS
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    import plotly.graph_objects as go
    import pandas as pd

    # ── fetch data ────────────────────────────────────────────────────────
    cust_kpi_df = run_query(conn, """
        SELECT
            round(avg(customer_rating), 2)              as avg_cust_rating,
            sum(case when is_cancelled_by_customer = true
                     then 1 else 0 end)                 as cust_cancels,
            sum(case when lower(trim(booking_status_raw)) = 'no driver found'
                     then 1 else 0 end)                 as no_driver_found,
            count(*)                                    as total_bookings
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
    """)

    top_spender_df = run_query(conn, """
        SELECT customer_id, lifetime_spend_inr
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_customer_segments
        ORDER BY lifetime_spend_inr DESC
        LIMIT 1
    """)

    top10_df = run_query(conn, """
        SELECT customer_id, lifetime_spend_inr
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_customer_segments
        ORDER BY lifetime_spend_inr DESC
        LIMIT 10
    """)

    cust_cancel_df = run_query(conn, """
        SELECT
            customer_cancel_reason,
            sum(total_cancels) as cnt
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_cancellation_insights
        WHERE customer_cancel_reason IS NOT NULL
          AND lower(trim(customer_cancel_reason)) != 'null'
        GROUP BY customer_cancel_reason
        ORDER BY cnt DESC
        LIMIT 5
    """)

    locations_df = run_query(conn, """
        SELECT
            pickup_location,
            count(*) as total_pickups
        FROM dbt_uber_analytics_catalog.dbt_asawant_staging.stg_bookings
        WHERE pickup_location IS NOT NULL
        GROUP BY pickup_location
        ORDER BY total_pickups DESC
        LIMIT 10
    """)

    # ── compute KPIs ──────────────────────────────────────────────────────
    avg_cust_rating  = float(cust_kpi_df["avg_cust_rating"].iloc[0] or 0)
    cust_cancels     = int(cust_kpi_df["cust_cancels"].iloc[0] or 0)
    no_driver        = int(cust_kpi_df["no_driver_found"].iloc[0] or 0)
    total_bookings   = int(cust_kpi_df["total_bookings"].iloc[0] or 0)
    cust_cancel_pct  = round(cust_cancels / total_bookings * 100) if total_bookings else 0
    no_driver_pct    = round(no_driver / total_bookings * 100) if total_bookings else 0
    top_cid          = str(top_spender_df["customer_id"].iloc[0]) if not top_spender_df.empty else "—"
    top_spend        = float(top_spender_df["lifetime_spend_inr"].iloc[0]) if not top_spender_df.empty else 0

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    for col, title, value, sub in [
        (k1, "AVG CUST. RATING",    f"{avg_cust_rating:.2f}",      "Out of 5.0"),
        (k2, "CUST. CANCELLATIONS", f"{cust_cancels:,}",           f"{cust_cancel_pct}% of bookings"),
        (k3, "TOP CUSTOMER SPEND",  f"₹{int(top_spend):,}",        top_cid),
        (k4, "NO DRIVER FOUND",     f"{no_driver:,}",              f"{no_driver_pct}% unserviced"),
    ]:
        col.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;
                    border-radius:10px;padding:1.1rem 1.25rem">
            <div style="font-size:0.68rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.4rem">{title}</div>
            <div style="font-size:1.85rem;font-weight:700;color:#000;
                        line-height:1.1;margin-bottom:0.2rem">{value}</div>
            <div style="font-size:0.78rem;color:#767676">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── top 10 customers by lifetime spend ───────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">Top 10 customers by lifetime spend</div>
    """, unsafe_allow_html=True)

    top10_sorted = top10_df.sort_values("lifetime_spend_inr", ascending=True)
    fig_top10 = go.Figure(go.Bar(
        x=top10_sorted["lifetime_spend_inr"],
        y=top10_sorted["customer_id"],
        orientation="h",
        marker_color="#7B61FF",
        hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>"
    ))
    fig_top10.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            showgrid=True, gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickprefix="₹", tickformat=","
        ),
        yaxis=dict(
            showgrid=False, linecolor="#E6E6E6",
            tickfont=dict(color="#333", size=11)
        ),
        showlegend=False,
        bargap=0.25
    )
    st.plotly_chart(fig_top10, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── customer cancellation reasons ─────────────────────────────────────
    st.markdown("""
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem;margin-bottom:16px">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.75rem">Customer cancellation reasons</div>
    """, unsafe_allow_html=True)

    fig_ccancel = go.Figure(go.Bar(
        x=cust_cancel_df["customer_cancel_reason"],
        y=cust_cancel_df["cnt"],
        marker_color="#276EF1",
        hovertemplate="%{x}<br>%{y:,}<extra></extra>"
    ))
    fig_ccancel.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            showgrid=False, linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=12)
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F0F0F0",
            linecolor="#E6E6E6",
            tickfont=dict(color="#767676", size=11),
            tickformat=","
        ),
        showlegend=False,
        bargap=0.35
    )
    st.plotly_chart(fig_ccancel, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── top 10 pickup locations ────────────────────────────────────────────
    total_pickups_all = int(locations_df["total_pickups"].sum())

    loc_rows = ""
    for _, row in locations_df.iterrows():
        share = row["total_pickups"] / total_pickups_all * 100 if total_pickups_all else 0
        loc_rows += (
            '<tr style="border-bottom:1px solid #F0F0F0">'
            '<td style="padding:0.65rem 0.75rem;color:#000;font-weight:500">'
            + str(row["pickup_location"]) +
            '</td>'
            '<td style="padding:0.65rem 0.75rem;color:#333">'
            + f"{int(row['total_pickups']):,}" +
            '</td>'
            '<td style="padding:0.65rem 0.75rem">'
            '<span style="background:#EEF2FF;color:#276EF1;font-size:0.78rem;'
            'font-weight:600;padding:0.2rem 0.6rem;border-radius:99px">'
            + f"{share:.2f}%" +
            '</span>'
            '</td>'
            '</tr>'
        )

    locations_html = """
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:1rem">Top 10 pickup locations by demand</div>
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem">
            <thead>
                <tr style="border-bottom:1.5px solid #E8E8E5">
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Location</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Total pickups</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Share</th>
                </tr>
            </thead>
            <tbody>
                LOC_ROWS
            </tbody>
        </table>
    </div>
    """.replace("LOC_ROWS", loc_rows)

    st.markdown(locations_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — PAYMENTS
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    import plotly.graph_objects as go

    pay_df = run_query(conn, """
        SELECT
            payment_method,
            sum(completed_rides)        as total_rides,
            sum(total_revenue_inr)      as total_revenue_inr,
            round(avg(avg_fare_inr), 0) as avg_fare_inr
        FROM dbt_uber_analytics_catalog.dbt_asawant_marts.mart_revenue_summary
        GROUP BY payment_method
        ORDER BY total_rides DESC
    """)

    total_rides_all = int(pay_df["total_rides"].sum())

    pay_df["share_pct"] = (
        pay_df["total_rides"] / total_rides_all * 100
    ).round(1)

    # classify payment type
    digital_methods = ["upi", "credit card", "debit card", "uber wallet",
                       "wallet", "card"]

    def payment_type(method):
        if str(method).lower().strip() in ["cash"]:
            return "Offline"
        return "Digital"

    pay_df["payment_type"] = pay_df["payment_method"].apply(payment_type)

    def fmt_cr(v):
        return f"₹{v/1e7:.2f}Cr"

    # ── find specific payment method shares for KPIs ───────────────────────
    def get_share(keyword):
        match = pay_df[
            pay_df["payment_method"].str.lower().str.contains(keyword, na=False)
        ]
        if match.empty:
            return 0.0, 0
        return float(match["share_pct"].iloc[0]), int(match["total_rides"].iloc[0])

    upi_pct,    upi_rides    = get_share("upi")
    cash_pct,   cash_rides   = get_share("cash")
    wallet_pct, wallet_rides = get_share("wallet")

    # card = credit + debit combined
    card_df = pay_df[pay_df["payment_method"].str.lower().str.contains("card", na=False)]
    card_pct   = round(card_df["share_pct"].sum(), 1)
    card_rides = int(card_df["total_rides"].sum())

    # ── KPI cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    for col, title, value, sub in [
        (k1, "UPI SHARE",    f"{upi_pct}%",    f"{upi_rides:,} rides"),
        (k2, "CASH SHARE",   f"{cash_pct}%",   f"{cash_rides:,} rides"),
        (k3, "WALLET SHARE", f"{wallet_pct}%", f"{wallet_rides:,} rides"),
        (k4, "CARD SHARE",   f"{card_pct}%",   f"{card_rides:,} rides"),
    ]:
        col.markdown(f"""
        <div style="background:#F9F9F7;border:1px solid #E8E8E5;
                    border-radius:10px;padding:1.1rem 1.25rem">
            <div style="font-size:0.68rem;font-weight:600;color:#767676;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.4rem">{title}</div>
            <div style="font-size:1.85rem;font-weight:700;color:#000;
                        line-height:1.1;margin-bottom:0.2rem">{value}</div>
            <div style="font-size:0.78rem;color:#767676">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── donut + horizontal bar ─────────────────────────────────────────────
    PAYMENT_COLORS = [
        "#1AC8A1","#888780","#7B61FF",
        "#276EF1","#E74C3C","#E67E22"
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">Payment method distribution</div>
        """, unsafe_allow_html=True)

        labels_pct = [
            f"{row['payment_method']} {row['share_pct']}%"
            for _, row in pay_df.iterrows()
        ]

        fig_donut = go.Figure(go.Pie(
            labels=labels_pct,
            values=pay_df["total_rides"],
            hole=0.52,
            marker_colors=PAYMENT_COLORS[:len(pay_df)],
            textinfo="none",
            hovertemplate="%{label}<br>%{value:,} rides<extra></extra>"
        ))
        fig_donut.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(
                orientation="h",
                x=0, y=1.15,
                font=dict(size=11, color="#000"),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                    padding:1.25rem 1.5rem">
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">Payment method by volume</div>
        """, unsafe_allow_html=True)

        pay_sorted = pay_df.sort_values("total_rides", ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=pay_sorted["total_rides"],
            y=pay_sorted["payment_method"],
            orientation="h",
            marker_color=PAYMENT_COLORS[:len(pay_sorted)][::-1],
            hovertemplate="%{y}<br>%{x:,} rides<extra></extra>"
        ))
        fig_bar.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis=dict(
                showgrid=True, gridcolor="#F0F0F0",
                linecolor="#E6E6E6",
                tickfont=dict(color="#767676", size=11),
                tickformat=","
            ),
            yaxis=dict(
                showgrid=False, linecolor="#E6E6E6",
                tickfont=dict(color="#333", size=12)
            ),
            showlegend=False,
            bargap=0.25
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── payment method detail table ────────────────────────────────────────
    table_rows = ""
    for i, (_, row) in enumerate(pay_df.iterrows()):
        ptype       = payment_type(row["payment_method"])
        badge_bg    = "#ECFDF5" if ptype == "Digital" else "#FFF7ED"
        badge_color = "#065F46" if ptype == "Digital" else "#92400E"
        table_rows += (
            '<tr style="border-bottom:1px solid #F0F0F0">'
            '<td style="padding:0.7rem 0.75rem;font-weight:500;color:#000">'
            + str(row["payment_method"]) +
            '</td>'
            '<td style="padding:0.7rem 0.75rem;color:#333">'
            + f"{int(row['total_rides']):,}" +
            '</td>'
            '<td style="padding:0.7rem 0.75rem;color:#333">'
            + f"{row['share_pct']}%" +
            '</td>'
            '<td style="padding:0.7rem 0.75rem;color:#333">'
            + fmt_cr(row["total_revenue_inr"]) +
            '</td>'
            '<td style="padding:0.7rem 0.75rem">'
            '<span style="background:' + badge_bg + ';color:' + badge_color + ';'
            'font-size:0.78rem;font-weight:600;padding:0.2rem 0.7rem;'
            'border-radius:99px">' + ptype + '</span>'
            '</td>'
            '</tr>'
        )

    detail_html = """
    <div style="background:#fff;border:1px solid #E8E8E5;border-radius:12px;
                padding:1.25rem 1.5rem">
        <div style="font-size:0.72rem;font-weight:700;color:#000;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:1rem">Payment method detail</div>
        <table style="width:100%;border-collapse:collapse;font-size:0.88rem">
            <thead>
                <tr style="border-bottom:1.5px solid #E8E8E5">
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Method</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Rides</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Share</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Est. revenue</th>
                    <th style="text-align:left;padding:0.5rem 0.75rem;font-size:0.7rem;
                               font-weight:600;color:#767676;text-transform:uppercase;
                               letter-spacing:0.06em">Trend</th>
                </tr>
            </thead>
            <tbody>
                TABLE_ROWS
            </tbody>
        </table>
    </div>
    """.replace("TABLE_ROWS", table_rows)

    st.markdown(detail_html, unsafe_allow_html=True)



# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — AI INSIGHTS
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    from utils.ai_agent import generate_sql, generate_insight
    import plotly.express as px
    import plotly.graph_objects as go

    # ── header ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#000;border-radius:12px;padding:1.5rem 2rem;
                margin-bottom:1.5rem">
        <div style="font-size:0.7rem;font-weight:600;color:#FFCD00;
                    text-transform:uppercase;letter-spacing:0.1em;
                    margin-bottom:0.4rem">
            Powered by Groq · Llama 3.3 70B · completely free
        </div>
        <div style="font-size:1.4rem;font-weight:700;color:#fff;
                    margin-bottom:0.3rem">
            Ask anything about the Uber NCR data
        </div>
        <div style="font-size:0.85rem;color:#999">
            Groq writes the SQL · Databricks runs it · AI explains the results
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── example questions ─────────────────────────────────────────────────
    EXAMPLES = [
        "Which vehicle type generates most revenue per km?",
        "Top 10 pickup locations by cancellation rate",
        "Which hour of day has highest booking volume?",
        "Compare avg driver rating by payment method",
        "Which customers have highest lifetime spend?",
        "Revenue trend for Auto vs Go Mini by month",
        "Which cancellation reason has longest avg wait?",
        "Locations with most no driver found incidents",
    ]

    st.markdown("""
    <div style="font-size:0.72rem;font-weight:700;color:#000;
                text-transform:uppercase;letter-spacing:0.08em;
                margin-bottom:0.75rem">
        Try these questions
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, q in enumerate(EXAMPLES):
        if cols[i % 4].button(q, key=f"ai_ex_{i}"):
            st.session_state["ai_question"] = q

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── input ─────────────────────────────────────────────────────────────
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        question = st.text_input(
            "question",
            value=st.session_state.get("ai_question", ""),
            placeholder="e.g. Which vehicle type has the worst driver cancellation rate?",
            label_visibility="collapsed",
            key="ai_question_input"
        )
    with col_btn:
        ask = st.button("Ask →", type="primary",
                        use_container_width=True, key="ai_ask_btn")

    # ── agent loop ────────────────────────────────────────────────────────
    if ask and question:

        # step 1 — generate SQL
        with st.spinner("Writing SQL with Llama 3.3 70B..."):
            try:
                sql_text = generate_sql(question)
            except Exception as e:
                st.error(f"SQL generation failed: {e}")
                st.stop()

        # step 2 — run against Databricks
        with st.spinner("Querying Databricks..."):
            try:
                df = run_query(conn, sql_text)
            except Exception as e:
                st.error(f"Query failed: {e}")
                st.info("The SQL might reference wrong column names. Try rephrasing.")
                st.stop()

        if df.empty:
            st.warning("Query returned no rows.")
            st.stop()

        # step 3 — results + chart side by side
        col1, col2 = st.columns([3, 2])

        # step 3 — AI analysis full width
        with st.spinner("Analysing with Groq..."):
            try:
                insight = generate_insight(question, sql_text, df)
                st.markdown(
                    '<div style="background:#FFFBEA;border:1.5px solid #FFCD00;'
                    'border-radius:12px;padding:1.25rem 1.5rem;'
                    'font-size:0.88rem;line-height:1.75;color:#000">'
                    + insight.replace("\n", "<br>") +
                    '</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.warning(f"Insight generation failed: {e}")

        # step 4 — auto chart
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        num_cols  = df.select_dtypes("number").columns.tolist()
        cat_cols  = df.select_dtypes("object").columns.tolist()
        date_cols = [c for c in df.columns if "date" in c.lower()]

        if len(df) > 1 and num_cols and (cat_cols or date_cols):
            st.markdown("""
            <div style="font-size:0.72rem;font-weight:700;color:#000;
                        text-transform:uppercase;letter-spacing:0.08em;
                        margin-bottom:0.75rem">Auto chart</div>
            """, unsafe_allow_html=True)

            x_col     = date_cols[0] if date_cols else cat_cols[0]
            y_col     = num_cols[0]

            chart_col1, chart_col2 = st.columns([4, 1])
            with chart_col2:
                chart_type = st.selectbox(
                    "Chart type",
                    ["Bar", "Line", "Scatter", "Pie"],
                    key="ai_chart_type"
                )

            with chart_col1:
                if chart_type == "Bar":
                    fig = go.Figure(go.Bar(
                        x=df[x_col], y=df[y_col],
                        marker_color="#000000"
                    ))
                elif chart_type == "Line":
                    fig = go.Figure(go.Scatter(
                        x=df[x_col], y=df[y_col],
                        mode="lines+markers",
                        line=dict(color="#000000", width=2.5),
                        marker=dict(color="#FFCD00", size=7)
                    ))
                elif chart_type == "Scatter":
                    fig = go.Figure(go.Scatter(
                        x=df[x_col], y=df[y_col],
                        mode="markers",
                        marker=dict(color="#276EF1", size=8)
                    ))
                else:
                    fig = go.Figure(go.Pie(
                        labels=df[x_col],
                        values=df[y_col],
                        hole=0.5,
                        marker_colors=[
                            "#000000","#FFCD00","#276EF1",
                            "#1AC8A1","#E74C3C","#888780"
                        ]
                    ))

                fig.update_layout(
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FFFFFF",
                    height=320,
                    margin=dict(l=10, r=10, t=20, b=10),
                    font=dict(family="DM Sans", color="#000"),
                    xaxis=dict(
                        showgrid=True, gridcolor="#F0F0F0",
                        linecolor="#E6E6E6",
                        tickfont=dict(color="#767676")
                    ),
                    yaxis=dict(
                        showgrid=True, gridcolor="#F0F0F0",
                        linecolor="#E6E6E6",
                        tickfont=dict(color="#767676")
                    ),
                    showlegend=(chart_type == "Pie")
                )
                st.plotly_chart(fig, use_container_width=True)

 