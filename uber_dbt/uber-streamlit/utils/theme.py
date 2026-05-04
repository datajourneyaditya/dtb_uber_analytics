import streamlit as st
import plotly.graph_objects as go


UBER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stApp"], .main, section.main {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #F6F6F6 !important;
    color: #000000 !important;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: #F6F6F6 !important;
}

.main .block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
    background-color: #F6F6F6 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}

h1, h2, h3, h4 {
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
}
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
h2, h3 {
    font-weight: 600 !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #000000 !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
    border-radius: 8px !important;
    padding: 0.4rem 0.75rem !important;
}
[data-testid="stSidebarNav"] a:hover {
    background-color: #1A1A1A !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #FFCD00 !important;
    color: #000000 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] * {
    color: #000000 !important;
}

[data-testid="metric-container"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E6E6E6 !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.5rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="stMetricLabel"] {
    color: #767676 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
    color: #000000 !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #1AC8A1 !important;
}

.stButton > button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    background-color: #333333 !important;
}
.stButton > button[kind="primary"] {
    background-color: #FFCD00 !important;
    color: #000000 !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #E6B800 !important;
}

.stTextInput > div > div > input {
    border: 1.5px solid #E6E6E6 !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    color: #000000 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #000000 !important;
    box-shadow: none !important;
}

.stSelectbox > div > div {
    border: 1.5px solid #E6E6E6 !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    color: #000000 !important;
}

[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1.5px solid #E6E6E6 !important;
    overflow: hidden !important;
}

.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E6E6E6 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: #000000 !important;
}
.streamlit-expanderContent {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E6E6E6 !important;
    border-top: none !important;
}

[data-testid="stInfo"] {
    background-color: #F0F5FF !important;
    border-left: 4px solid #276EF1 !important;
    color: #000000 !important;
    border-radius: 8px !important;
}

[data-testid="stCaptionContainer"] {
    color: #767676 !important;
}

hr {
    border-color: #E6E6E6 !important;
    margin: 1.5rem 0 !important;
}

.uber-section-header {
    background: #000000 !important;
    color: #FFFFFF !important;
    padding: 0.4rem 1rem !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    display: inline-block !important;
    margin-bottom: 0.75rem !important;
}
</style>
"""

COLORS = [
    "#000000", "#FFCD00", "#276EF1",
    "#1AC8A1", "#FF6B6B", "#767676",
    "#FF9500", "#5856D6"
]


def apply_theme():
    st.markdown(UBER_CSS, unsafe_allow_html=True)


def uber_header(title, subtitle=""):
    sub_html = ""
    if subtitle:
        sub_html = (
            "<p style='color:#767676;font-size:0.9rem;margin:0.25rem 0 0'>"
            + subtitle
            + "</p>"
        )
    st.markdown(
        "<div style='border-bottom:3px solid #FFCD00;"
        "padding-bottom:0.75rem;margin-bottom:1.5rem'>"
        "<h1 style='margin:0;padding:0;color:#000000 !important'>"
        + title
        + "</h1>"
        + sub_html
        + "</div>",
        unsafe_allow_html=True
    )


def uber_section(label):
    st.markdown(
        "<div class='uber-section-header'>" + label + "</div>",
        unsafe_allow_html=True
    )


def apply_plotly_theme(fig):
    fig.update_layout(
        template="plotly_white",
        colorway=COLORS,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", color="#000000"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            bgcolor="#FFFFFF",
            bordercolor="#E6E6E6",
            borderwidth=1,
            font=dict(color="#000000")
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#F0F0F0",
        linecolor="#E6E6E6",
        tickfont=dict(color="#767676"),
        title_font=dict(color="#000000")
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F0F0F0",
        linecolor="#E6E6E6",
        tickfont=dict(color="#767676"),
        title_font=dict(color="#000000")
    )
    return fig