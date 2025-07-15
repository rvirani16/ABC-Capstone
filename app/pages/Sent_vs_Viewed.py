# Sent_vs_Viewed.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Sent vs Viewed Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match Sent_Notification page
st.markdown("""
<style>
    .filter-title {
        color: #000000;
        font-size: 18px;
        margin-bottom: 15px;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
    .row-widget.stButton {
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #90cdf4;
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        color: #000000;
        text-align: center;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df_sent = pd.read_csv('./datasets/notifications_users.csv', parse_dates=['start'])
        df_viewed = pd.read_csv('./datasets/Combined_views.csv', parse_dates=['View_time'])
        return df_sent, df_viewed
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df_sent, df_viewed = load_data()

if df_sent is not None and df_viewed is not None:
    # Sidebar filters
    with st.sidebar:
        st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

        # Role filter
        role_titles = df_sent['tile_roles'].dropna().unique()
        role_options = ["All"] + sorted(role_titles)
        selected_role = st.selectbox("Role Title", role_options)

        # Year filter
        sent_years = df_sent['start'].dt.year.dropna().unique()
        viewed_years = df_viewed['View_time'].dt.year.dropna().unique()
        all_years = sorted(set(sent_years) | set(viewed_years))
        year_options = ["All"] + [str(y) for y in all_years]
        selected_year = st.selectbox("Year", year_options)



    # Main content
    st.title("Sent vs Viewed Analytics")

    # Apply filters
    if selected_role != "All":
        filtered_users = df_sent[df_sent['tile_roles'] == selected_role]['capstone_email'].unique()
        df_sent_filtered = df_sent[df_sent['capstone_email'].isin(filtered_users)].copy()
        df_viewed_filtered = df_viewed[df_viewed['email'].isin(filtered_users)].copy()
    else:
        df_sent_filtered = df_sent.copy()
        df_viewed_filtered = df_viewed.copy()

    if selected_year != "All":
        selected_year = int(selected_year)
        df_sent_filtered = df_sent_filtered[df_sent_filtered['start'].dt.year == selected_year]
        df_viewed_filtered = df_viewed_filtered[df_viewed_filtered['View_time'].dt.year == selected_year]

    # Add Month columns
    df_sent_filtered['Month'] = df_sent_filtered['start'].dt.to_period("M")
    df_viewed_filtered['Month'] = df_viewed_filtered['View_time'].dt.to_period("M")

    # Apply exclusions
    exclude_sent_months = [pd.Period("2023-12", freq="M"), pd.Period("2025-01", freq="M")]
    df_sent_filtered = df_sent_filtered[~df_sent_filtered['Month'].isin(exclude_sent_months)]
    df_viewed_filtered = df_viewed_filtered[df_viewed_filtered['View_time'].dt.year != 2025]
    df_viewed_chart = df_viewed_filtered[df_viewed_filtered['Month'] != pd.Period("2023-12", freq="M")]

    # Calculate metrics
    total_sent = len(df_sent_filtered)
    total_viewed = df_viewed_filtered['count'].sum()

    # Display metrics
    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.markdown(f'<div class="metric-value">{total_sent:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Notifications Sent</div>', unsafe_allow_html=True)

    with metric_col2:
        st.markdown(f'<div class="metric-value">{total_viewed:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Notifications Viewed</div>', unsafe_allow_html=True)

    # Prepare chart data
    monthly_sent = df_sent_filtered['Month'].value_counts().sort_index()
    monthly_viewed = df_viewed_chart.groupby('Month')['count'].sum().sort_index()

    # Create chart
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(
        x=monthly_sent.index.to_timestamp(),
        y=monthly_sent.values,
        mode='lines+markers',
        name='Notifications Sent',
        line=dict(color='#1a365d'),
        marker=dict(symbol='circle'),
        hovertemplate='Month: %{x|%b %Y}<br>Sent: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=monthly_viewed.index.to_timestamp(),
        y=monthly_viewed.values,
        mode='lines+markers',
        name='Notifications Viewed',
        line=dict(color='#90cdf4'),
        marker=dict(symbol='square'),
        hovertemplate='Month: %{x|%b %Y}<br>Viewed: %{y}<extra></extra>'
    ))

    # layout
    title_role = selected_role if selected_role != "All" else "All Roles"
    fig.update_layout(
        title=dict(
            text=f"Monthly Distribution for {title_role}",
            font=dict(color='black', size=20)
        ),
        xaxis=dict(
            title=dict(
                text="Month",
                font=dict(color='black', size=14)  # X-axis label color and size
            ),
            showgrid=True,
            gridcolor='#E5E5E5',
            linecolor='lightgray',  # X-axis line color
            tickcolor='lightgray',  # X-axis tick color
            tickfont=dict(color='black')  # X-axis tick labels color
        ),
        yaxis=dict(
            title=dict(
                text="Count",
                font=dict(color='black', size=14)  # Y-axis label color and size
            ),
            showgrid=True,
            gridcolor='#E5E5E5',
            linecolor='lightgray',  # Y-axis line color
            tickcolor='lightgray',  # Y-axis tick color
            tickfont=dict(color='black')  # Y-axis tick labels color
        ),
        legend=dict(
            title=dict(
                text="Metric",
                font=dict(color='black', size=14)  # Legend title color and size
            ),
            font=dict(color='black', size=12),  # Legend text color and size
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)"
        ),
        width=1400,
        height=400,
        margin=dict(l=60, r=40, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Unable to load data. Please check the data files and try again.")