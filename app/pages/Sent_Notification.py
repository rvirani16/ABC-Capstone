# notification_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Set page config
st.set_page_config(
    page_title="Notification Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .filter-title {
        color: #000000;
        font-size: 18px;
        margin-bottom: 15px;
    }
    /* Hide main page scrollbar */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
    /* Reduce spacing */
    .row-widget.stButton {
        margin-bottom: 10px;
    }
    /* Adjust header spacing */
    h1, h2, h3 {
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    /* Make charts fit in container */
    .js-plotly-plot, .plotly, .plot-container {
        height: 100% !important;
        width: 100% !important;
    }
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    /* Chart container height */
    .chart-area {
        height: calc(100vh - 200px);
    }
    /* KPI styling without boxes */
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #90cdf4;
        text-align: center;
    }
    .kpi-label {
        font-size: 14px;
        color: #000000;
        text-align: center;
        margin-bottom: 15px;
    }
    .navigation-button {
        background-color: #90cdf4;
        color: #1a365d;
        padding: 10px 15px;
        border-radius: 5px;
        text-align: center;
        margin: 5px 0;
        cursor: pointer;
        border: 1px solid #90cdf4;
    }
    .navigation-button:hover {
        background-color: #63b3ed;
    }
    .selected-nav {
        background-color: #1a365d;
        color: white;
    }
    
    data-baseweb="tag"] {
        background-color: white !important;
        border: 1px solid rgba(144, 205, 244, 0.4) !important;  /* Lighter, more subtle border */
        border-radius: 6px !important;  /* Soft rounded edges */
        padding: 2px 8px !important;
        
    }

    /* Style for tag text */
    [data-baseweb="tag"] span {
        color: black !important;
    }

    /* Style for tag close button */
    [data-baseweb="tag"] button {
        color: black !important;
    }

    /* Style for the multiselect dropdown and input */
    [data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;  /* Subtle border */
        border-radius: 6px !important;
    }

    /* Style for selected items in dropdown */
    [data-baseweb="select"] [data-baseweb="selected-option"] {
        color: black !important;
    }

    /* Style for dropdown menu */
    [data-baseweb="popover"] {
        border-radius: 6px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }

    /* Style for dropdown options */
    [data-baseweb="menu"] {
        border-radius: 6px !important;
    }
    
    .stMultiSelect > div[data-baseweb="select"] > div {
        background-color: white !important;
    }

    /* Style for the selected value text */
    .stMultiSelect > div[data-baseweb="select"] span {
        color: black !important;
    }

    /* Style for the selected tag in dropdown */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid rgba(255, 0, 0, 0.0) !important;
        border-radius: 6px !important;
    }

    /* Style for the selected tag text */
    .stMultiSelect [data-baseweb="tag"] span {
        color: black !important;
    }

    /* Style for the close (x) button in selected tag */
    .stMultiSelect [data-baseweb="tag"] button {
        color: black !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Move filters to sidebar
with st.sidebar:
    st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

    # Load data
    @st.cache_data
    def load_data():
        try:
            '''df1 = pd.read_csv('./datasets/hub_notifications_transformed.csv')'''
            '''df2 = pd.read_csv('./datasets/notifications_with_tiles.csv')'''
            dir_path_1 = os.path.dirname(os.path.abspath(__file__))
            file_path_1 = os.path.join(dir_path_1, "..", "datasets", "hub_notifications_transformed.csv")
            df1 = pd.read_csv(file_path_1)

            dir_path_2 = os.path.dirname(os.path.abspath(__file__))
            file_path_2 = os.path.join(dir_path_2, "..", "datasets", "notifications_with_tiles.csv")
            df2 = pd.read_csv(file_path_2)

            

            # Convert date columns to datetime
            df1['start'] = pd.to_datetime(df1['start'], errors='coerce')
            df1['end'] = pd.to_datetime(df1['end'], errors='coerce')
            df2['start'] = pd.to_datetime(df2['start'], errors='coerce')
            df2['end'] = pd.to_datetime(df2['end'], errors='coerce')

            # Extract month and year for both dataframes
            df1['month_year'] = df1['start'].dt.strftime('%b %Y')
            df2['month_year'] = df2['start'].dt.strftime('%b %Y')

            # Create a mapping from tile_id to tile_name using df2
            tile_mapping = df2[['tile_id', 'tile_name']].drop_duplicates()
            tile_id_to_name = dict(zip(tile_mapping['tile_id'].astype(str), tile_mapping['tile_name']))

            # Map df1's tile (which contains tile_id) to tile_name using the mapping
            df1['tile_name'] = df1['tile'].astype(str).map(tile_id_to_name)

            return df1, df2
        except Exception as e:
            st.error(f"Error loading data: {e}")
            # Create sample data for demonstration
            df1 = pd.DataFrame({
                'notification_type': ['major', 'major', 'major', 'minor', 'minor'],
                'time_diff_days': [7.0, 7.0, 7.7, 0.1, 0.2],
                'start': pd.date_range(start='2023-06-01', periods=5, freq='D'),
                'tile': ['1', '2', '1', '3', '2']
            })
            df1['month_year'] = df1['start'].dt.strftime('%b %Y')

            df2 = pd.DataFrame({
                'notification_type': ['minor', 'minor', 'minor', 'minor', 'minor'],
                'time_diff_days': [0.1, 0.1, 0.2, 0.3, 0.1],
                'start': pd.date_range(start='2023-07-01', periods=5, freq='15D'),
                'tile_id': ['1', '2', '3', '1', '2'],
                'tile_name': ['Dashboard A', 'Dashboard B', 'Dashboard C', 'Dashboard A', 'Dashboard B']
            })
            df2['month_year'] = df2['start'].dt.strftime('%b %Y')

            return df1, df2

    df1, df2 = load_data()

    # Get unique notification types
    notification_types = sorted(list(set(df1['notification_type'].unique()) | set(df2['notification_type'].unique())))

    # Multiselect for notification types
    selected_types = st.multiselect(
        "Notification Type",
        options=notification_types,
        default=notification_types
    )

    # Get unique tile names from df2 (notifications_with_tiles)
    all_tile_names = sorted(df2['tile_name'].unique())
    tile_options = ["All"] + all_tile_names

    # Multiselect for tile names with "All" option
    selected_tile_names = st.multiselect(
        "Tile Name",
        options=tile_options,
        default=["All"]
    )

     # Generate month-year options from Jul 2023 to Dec 2024
    def generate_month_year_options():
        month_year_options = []
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # 2023 (July to December)
        for month in range(6, 12):  # 6 = July (0-based index)
            month_year_options.append(f"{month_names[month]} 2023")

        # 2024 (January to December)
        for month in range(12):
            month_year_options.append(f"{month_names[month]} 2024")

        return ["All"] + month_year_options

    # Get month-year options
    month_year_options = generate_month_year_options()

    # Multiselect for month-year with "All" option
    selected_month_years = st.multiselect(
        "Month-Year",
        options=month_year_options,
        default=["All"]
    )

    
    
# Main content
st.title("Notification Dashboard")

# Apply filters for notification types
filtered_df1 = df1[df1['notification_type'].isin(selected_types)]
filtered_df2 = df2[df2['notification_type'].isin(selected_types)]

# Apply tile name filter
if "All" not in selected_tile_names:
    filtered_df1 = filtered_df1[filtered_df1['tile_name'].isin(selected_tile_names)]
    filtered_df2 = filtered_df2[filtered_df2['tile_name'].isin(selected_tile_names)]

# Apply month-year filter
if "All" not in selected_month_years:
    filtered_df1 = filtered_df1[filtered_df1['month_year'].isin(selected_month_years)]
    filtered_df2 = filtered_df2[filtered_df2['month_year'].isin(selected_month_years)]

# Calculate KPIs
total_notifications = len(filtered_df1) + len(filtered_df2)

# Calculate average duration for major notifications
major_notifications_df1 = filtered_df1[filtered_df1['notification_type'] == 'major']
major_notifications_df2 = filtered_df2[filtered_df2['notification_type'] == 'major']
major_durations = pd.concat([major_notifications_df1['time_diff_days'],
                           major_notifications_df2['time_diff_days']])
avg_major_duration = major_durations.mean() if not major_durations.empty else 0

# Calculate average duration for minor notifications
minor_notifications_df1 = filtered_df1[filtered_df1['notification_type'] == 'minor']
minor_notifications_df2 = filtered_df2[filtered_df2['notification_type'] == 'minor']
minor_durations = pd.concat([minor_notifications_df1['time_diff_days'],
                           minor_notifications_df2['time_diff_days']])
avg_minor_duration = minor_durations.mean() if not minor_durations.empty else 0

# Display KPIs without background boxes
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f'<div class="kpi-value">{total_notifications}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Total Notifications</div>', unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f'<div class="kpi-value">{avg_major_duration:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Avg. Duration Major (Days)</div>', unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f'<div class="kpi-value">{avg_minor_duration:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-label">Avg. Duration Minor (Days)</div>', unsafe_allow_html=True)

# Charts with 40:60 split
chart_col1, chart_col2 = st.columns([4, 6])

with chart_col1:
    with st.container():
        st.subheader("Notification Types Distribution")

        # Prepare data for doughnut chart
        type_counts = filtered_df1['notification_type'].value_counts().reset_index()
        type_counts.columns = ['notification_type', 'count']

        # Create doughnut chart with reduced size
        fig1 = px.pie(
            type_counts,
            values='count',
            names='notification_type',
            hole=0.5,
            color='notification_type',
            color_discrete_map={'major': '#1a365d', 'minor': '#90cdf4'}
        )

        fig1.update_layout(
        showlegend=True,
        legend=dict(
            title=dict(
                text="Notification Type",
                font=dict(color='black', size=14)
            ),
            font=dict(color='black', size=12),
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(t=30, b=30, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black'),
        autosize=True,
        height=350
        )

        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with chart_col2:
    with st.container():
        st.subheader("Monthly Notification Trends")

        # Prepare data for clustered bar chart
        monthly_data = filtered_df2.groupby(['month_year', 'notification_type']).size().reset_index(name='count')

        # Sort by date
        try:
            # Convert month_year strings to datetime for proper sorting
            month_year_dt = {my: datetime.strptime(my, '%b %Y') for my in monthly_data['month_year'].unique()}
            month_order = sorted(monthly_data['month_year'].unique(), key=lambda x: month_year_dt[x])
        except:
            month_order = sorted(monthly_data['month_year'].unique())

        # Create clustered bar chart
        fig2 = px.bar(
            monthly_data,
            x='month_year',
            y='count',
            color='notification_type',
            color_discrete_map={'major': '#1a365d', 'minor': '#90cdf4'},
            category_orders={"month_year": month_order},
            barmode='group'  # Clustered bar chart
        )

        fig2.update_layout(
            xaxis=dict(
                title=dict(
                    text="Month",
                    font=dict(color='black', size=14)
                ),
                showgrid=True,
                gridcolor='#E5E5E5',
                linecolor='lightgray',
                tickcolor='lightgray',
                tickfont=dict(color='black')
            ),
            yaxis=dict(
                title=dict(
                    text="Number of Notifications",
                    font=dict(color='black', size=14)
                ),
                showgrid=True,
                gridcolor='#E5E5E5',
                linecolor='lightgray',
                tickcolor='lightgray',
                tickfont=dict(color='black')
            ),
            legend=dict(
                title=dict(
                    text="Notification Type",
                    font=dict(color='black', size=14)
                ),
                font=dict(color='black', size=12),
                orientation="v",
                yanchor="top",
                y=1.0,
                xanchor="right",
                x=1.0,
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(t=30, b=30, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black'),
            autosize=True,
            height=400
        )

        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})