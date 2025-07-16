import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import plotly.express as px
import os

# -------------------- Page Config & Styling --------------------
st.set_page_config(
    page_title="Dashboard Usage Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

pastel_colors = [
    '#90cdf4', '#fef08a', '#1a365d', '#a7f3d0', '#fecaca',
    '#dbeafe', '#fde68a', '#c7d2fe', '#bbf7d0', '#fca5a5',
    '#e0f2fe', '#fcd34d', '#e2e8f0'
]

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "..", "datasets", "answers_log_cleaned_1.csv")
    df = pd.read_csv(file_path)
    df['Start Timestamp'] = pd.to_datetime(df['Start Timestamp'], errors='coerce')
    df['Subject Area Name'] = df['Subject Area Name'].fillna('Unknown')
    df['Parsed Dashboard Name'] = df['Parsed Dashboard Name'].fillna('Unknown')
    df['Parsed Source Path Name'] = df['Parsed Source Path Name'].fillna('Unknown')
    df['Dashboard Page'] = df['Dashboard Page'].fillna('Unknown')
    return df

def load_data_binning():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "..", "datasets", "dashboard_usage_summary_by_bin 2.csv")
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    df['Distinct Users'] = pd.to_numeric(df['Distinct Users'], errors='coerce')
    df.dropna(subset=['Distinct Users'], inplace=True)
    df['Dashboard Name Cleaned'] = df['Dashboard Name'].apply(lambda x: str(x).strip().split("/")[-1])
    return df

# Load datasets
df = load_data()
df2 = load_data_binning()

with st.sidebar:
    st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

    subject_area_options = sorted(df['Subject Area Name'].dropna().unique())
    subject_area_options_with_all = ["All"] + subject_area_options
    selected_subject = st.selectbox("Select Subject Area", options=subject_area_options_with_all, index=0)

    # If 'All' is selected, use all subject areas
    selected_subjects = subject_area_options if selected_subject == "All" else [selected_subject]

    if selected_subjects:
        filtered_df = df[df['Subject Area Name'].isin(selected_subjects)]
        filtered_df2 = df2[df2['Subject Area Name'].isin(selected_subjects)]
    else:
        filtered_df = df.copy()
        filtered_df2 = df2.copy()

    dash_options = ["All"] + sorted(filtered_df['Parsed Dashboard Name'].unique())
    selected_dashboard = st.selectbox("Dashboard Name", options=dash_options)

    if selected_dashboard != "All":
        filtered_df = filtered_df[filtered_df['Parsed Dashboard Name'] == selected_dashboard]



# -------------------- KPI Metrics --------------------
st.title("Dashboard Usage Analytics")

latest_date = filtered_df['Start Timestamp'].max()
last_year = latest_date - timedelta(days=365)
last_30_days = latest_date - timedelta(days=30)
last_quarter = latest_date - timedelta(days=90)

def human_format(num, precision=2):
    if num is None:
        return "N/A"
    abs_num = abs(num)
    if abs_num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.{precision}f}B"
    elif abs_num >= 1_000_000:
        return f"{num / 1_000_000:.{precision}f}M"
    elif abs_num >= 1_000:
        return f"{num / 1_000:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"

def get_delta(series):
    if len(series) >= 2:
        current = series.iloc[-1]
        previous = series.iloc[-2]
        return round(((current - previous) / previous) * 100, 2) if previous != 0 else None
    return None


def format_change_arrow(value):
    if value is None:
        return "N/A"
    if value > 0:
        return f"<span style='color:green'>↑ {value:.2f}%</span>"
    elif value < 0:
        return f"<span style='color:red'>↓ {abs(value):.2f}%</span>"
    else:
        return f"<span>{value:.2f}%</span>"



total_views = filtered_df.shape[0]
total_reports = filtered_df['Parsed Source Path Name'].nunique()
total_users = filtered_df['User Name'].nunique()
views_365 = filtered_df[filtered_df['Start Timestamp'] >= last_year].shape[0]
views_30 = filtered_df[filtered_df['Start Timestamp'] >= last_30_days].shape[0]
views_90 = filtered_df[filtered_df['Start Timestamp'] >= last_quarter].shape[0]

yearly_views = filtered_df.groupby(filtered_df['Start Timestamp'].dt.to_period('Y')).size().sort_index()
monthly_views = filtered_df.groupby(filtered_df['Start Timestamp'].dt.to_period('M')).size().sort_index()
quarterly_views = filtered_df.groupby(filtered_df['Start Timestamp'].dt.to_period('Q')).size().sort_index()

yoy_change = get_delta(yearly_views)
mom_change = get_delta(monthly_views)
qoq_change = get_delta(quarterly_views)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-value">{total_reports:,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Reports Accessed</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-value">{total_users:,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Unique Users</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-value">{human_format(total_views)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Views</div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f'<div class="metric-value">{human_format(views_30)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">MoM Views ({format_change_arrow(mom_change)} )</div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-value">{human_format(views_90)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">QoQ Views ({format_change_arrow(qoq_change)} )</div>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<div class="metric-value">{human_format(views_365)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">YoY Views ({format_change_arrow(yoy_change)} )</div>', unsafe_allow_html=True)

# -------------------- Trend Chart --------------------
st.subheader("Usage Trend Over Time")
filtered_df['Time Group'] = filtered_df['Start Timestamp'].dt.to_period('M').dt.to_timestamp()
trend_data = filtered_df.groupby('Time Group').size().reset_index(name='Views')

bar_line_chart = px.bar(
    trend_data,
    x='Time Group',
    y='Views',
    color_discrete_sequence=pastel_colors,
    labels={'Time Group': 'Month', 'Views': 'Views'},
    title='Monthly Dashboard Views',
    opacity=0.6
)

bar_line_chart.add_scatter(
    x=trend_data['Time Group'],
    y=trend_data['Views'],
    mode='lines+markers',
    name='Trend',
    line=dict(color='black')
)

bar_line_chart.update_layout(
    height=400,
    showlegend=False,
    font=dict(color='black'),  # General font color
    xaxis=dict(
        fixedrange=True,
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        fixedrange=True,
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    )
)
st.plotly_chart(bar_line_chart, use_container_width=True)

# -------------------- Dashboard Category Breakdown --------------------
st.subheader("Dashboard Category Breakdown")
available_subjects_df2 = sorted(df2['Subject Area Name'].unique())
default_index = available_subjects_df2.index("Enterprise Data - Sales Dataset") if "Enterprise Data - Sales Dataset" in available_subjects_df2 else 0
selected_area_bins = st.selectbox("Select Subject Area for Category Breakdown", options=available_subjects_df2, index=default_index)

category_data = df2[df2['Subject Area Name'] == selected_area_bins]

category_counts = category_data['Dashboard Bin'].value_counts(normalize=True).reset_index()
category_counts.columns = ['Dashboard Bin', 'Percentage']
category_counts['Percentage'] *= 100

fig_bar = px.bar(
    category_counts,
    x='Dashboard Bin',
    y='Percentage',
    color='Dashboard Bin',
    color_discrete_sequence=pastel_colors,
    text=category_counts['Percentage'].map(lambda x: f"{x:.2f}%"),
    labels={'Percentage': 'Percentage'}
)

fig_bar.update_layout(
    title=f"Dashboard Bin Distribution for {selected_area_bins}",
    xaxis_title="Category",
    yaxis_title="Percentage",
    font=dict(color='black'),
    xaxis=dict(
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        title_font=dict(color='black'),
        tickfont=dict(color='black')
    )
)


st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("<br><br>", unsafe_allow_html=True)


# -------------------- Performance Summary --------------------
st.subheader("Performance by Subject Area")
access_counts = filtered_df.groupby('Subject Area Name').size().reset_index(name='Total Accesses')
unique_dashboards = filtered_df.groupby('Subject Area Name')['Dashboard Page'].nunique().reset_index(name='Dashboard Count')
subject_summary = pd.merge(access_counts, unique_dashboards, on='Subject Area Name')
subject_summary['Avg Views per Dashboard'] = (subject_summary['Total Accesses'] / subject_summary['Dashboard Count']).round(2)

access_median = subject_summary['Total Accesses'].median()
dash_median = subject_summary['Dashboard Count'].median()

def classify(row):
    if row['Dashboard Count'] > dash_median and row['Total Accesses'] < access_median:
        return 'Underutilized'
    elif row['Dashboard Count'] < dash_median and row['Total Accesses'] > access_median:
        return 'Over-utilized'
    else:
        return 'Normal'

subject_summary['Performance'] = subject_summary.apply(classify, axis=1)

overperformers = subject_summary[subject_summary['Performance'] == 'Over-utilized']
underperformers = subject_summary[subject_summary['Performance'] == 'Underutilized']

st.markdown("#### Overutilized Subject Areas")
st.dataframe(overperformers[['Subject Area Name', 'Dashboard Count', 'Total Accesses', 'Avg Views per Dashboard']])

st.markdown("#### Underutilized Subject Areas")
st.dataframe(underperformers[['Subject Area Name', 'Dashboard Count', 'Total Accesses', 'Avg Views per Dashboard']])
