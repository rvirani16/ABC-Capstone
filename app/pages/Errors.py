import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# -------------------- Page Config & Styling --------------------
st.set_page_config(
    page_title="Error Log Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

pastel_colors = [
    '#90cdf4', '#fef08a', '#1a365d', '#a7f3d0', '#fecaca',
    '#dbeafe', '#fde68a', '#c7d2fe', '#bbf7d0', '#fca5a5',
    '#e0f2fe', '#fcd34d', '#e2e8f0'
]

# Custom CSS to align with Sent_vs_Viewed style
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

# -------------------- Load Data --------------------
@st.cache_data

def load_data():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "..", "datasets", "error_file_cleaned_1.csv")
    df = pd.read_csv(file_path)
    if 'Start Timestamp' in df.columns:
        df['Date'] = pd.to_datetime(df['Start Timestamp'])
    elif 'Timestamp' in df.columns:
        df['Date'] = pd.to_datetime(df['StartTimestamp'])
    elif 'Error Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Error Date'])
    return df

# Load and prepare data
df = load_data()

# -------------------- Sidebar Filters --------------------
with st.sidebar:
    st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

    category_list = ["All"] + sorted(df["Error Category"].dropna().unique())
    selected_category = st.selectbox("Error Category", category_list)

    category_filtered = df if selected_category == "All" else df[df["Error Category"] == selected_category]

    subject_area_list = ["All"] + sorted(category_filtered["Subject Area Name"].dropna().unique())
    selected_subject = st.selectbox("Subject Area", subject_area_list)

    subject_filtered = category_filtered if selected_subject == "All" else category_filtered[category_filtered["Subject Area Name"] == selected_subject]

    # 🔽 Parsed Dashboard Name filtered *within* Subject Area
    dashboard_list = ["All"] + sorted(subject_filtered["Parsed Dashboard Name"].dropna().unique())
    selected_dashboard = st.selectbox("Dashboard Name", dashboard_list)

    dashboard_filtered = subject_filtered if selected_dashboard == "All" else subject_filtered[subject_filtered["Parsed Dashboard Name"] == selected_dashboard]

    if "Date" in dashboard_filtered.columns:
        min_date = dashboard_filtered["Date"].min().date()
        max_date = dashboard_filtered["Date"].max().date()
        start_date, end_date = st.date_input("Date Range", (min_date, max_date), min_value=min_date, max_value=max_date)
        filtered_df = dashboard_filtered[(dashboard_filtered["Date"].dt.date >= start_date) & (dashboard_filtered["Date"].dt.date <= end_date)]
    else:
        filtered_df = dashboard_filtered.copy()


# -------------------- Dashboard Title --------------------
st.title("Error Log Analytics Dashboard")

# -------------------- KPI Section --------------------
#st.subheader("Key Metrics")

total_errors = len(filtered_df)
total_records = 1436562
error_rate = (total_errors / total_records * 100) if total_records else 0
affected_users = filtered_df['User Name'].nunique() if 'User Name' in filtered_df.columns else "N/A"
affected_dashboards = filtered_df['Parsed Dashboard Name'].nunique() if 'Parsed Dashboard Name' in filtered_df.columns else "Parsed Dashboard Name"

most_impacted_area = (
    filtered_df['Subject Area Name'].value_counts().idxmax()
    if 'Subject Area Name' in filtered_df.columns and not filtered_df['Subject Area Name'].isna().all()
    else "N/A"
)

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-value">{total_errors:,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Errors Logged</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-value">{error_rate:.2f}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Error Rate</div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-value">{affected_users}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Affected Users</div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-value">{affected_dashboards}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Affected Dashboards</div>', unsafe_allow_html=True)

st.markdown(f'<div class="metric-label" style="text-align:left;">Most Impacted Subject Area: <span class="metric-value" style="font-size:14px; text-align:left;">{most_impacted_area}</span></div>', unsafe_allow_html=True)

# -------------------- Error Category Breakdown & Errors Over Time --------------------
col_cat, col_trend = st.columns([1, 2])

with col_cat:
    st.subheader("Errors by Category")
    category_counts = filtered_df["Error Category"].value_counts().reset_index()
    category_counts.columns = ["Error Category", "Count"]

    fig_category = px.bar(
        category_counts,
        x="Error Category",
        y="Count",
        color="Error Category",
        text="Count",  # Show counts on bars
        labels={"Count": "Number of Errors"},
        color_discrete_sequence=pastel_colors
    )

    fig_category.update_traces(
        textposition='outside'  # Display values above bars
    )

    fig_category.update_layout(
        height=600,
        showlegend=False,
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
    
    st.plotly_chart(fig_category, use_container_width=True)

with col_trend:
    st.subheader("Errors Over Time")
    if not filtered_df.empty and "Date" in filtered_df.columns:
        filtered_df["Month"] = filtered_df["Date"].dt.to_period("M")
        monthly_counts = filtered_df.groupby(["Month", "Error Category"]).size().reset_index(name="Count")
        monthly_counts["Month"] = monthly_counts["Month"].dt.to_timestamp()

        # Total errors per month (for the trend line)
        monthly_totals = monthly_counts.groupby("Month")["Count"].sum().reset_index()

        # Create figure with stacked bars
        fig_monthly = px.bar(
            monthly_counts,
            x="Month",
            y="Count",
            color="Error Category",
            barmode="stack",
            labels={"Count": "Number of Errors", "Month": "Month"},
            color_discrete_sequence=pastel_colors
        )

        # Add trend line as a scatter plot
        fig_monthly.add_scatter(
            x=monthly_totals["Month"],
            y=monthly_totals["Count"],
            mode="lines+markers",
            name="Trend",
            line=dict(color="black", width=2),
            marker=dict(size=6)
        )

        fig_monthly.update_layout(
            height=500,
            showlegend=False,
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
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.warning("Date column missing or no data available for trend analysis.")


st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------- Detailed Error Log --------------------
st.subheader("Detailed Error Log")
columns_to_show = [
   "Error Message"
]
filtered_df = filtered_df.rename(columns={"Error Text": "Error Message"})
display_df = filtered_df[columns_to_show]
column_rename_map = {"Error Text": "Error Message"}
display_df = filtered_df[columns_to_show].rename(columns={"Error Text": "Error Message"})

search_term = st.text_input("Search errors:", "")
if search_term:
    search_results = display_df[display_df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
    st.dataframe(search_results, use_container_width=True)
else:
    st.dataframe(display_df, use_container_width=True)

# Download button
csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Filtered Logs", data=csv, file_name="error_logs.csv", mime="text/csv")
