import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------- Page Setup --------------------
st.set_page_config(page_title="Overview Chart", layout="wide")
st.title("User Journey Mapping")

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
        text-align: center;
    }
    .kpi-label {
        font-size: 14px;
        color: #000000;
        text-align: center;
        margin-bottom: 15px;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Load Data --------------------
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, "..", "datasets", "user_level_with_names.csv")
df = pd.read_csv(file_path)

# -------------------- Sidebar Filters --------------------
st.sidebar.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)

all_titles = ['All'] + sorted(df['title'].dropna().unique().tolist())
selected_title = st.sidebar.selectbox("Select Title", all_titles)

all_quarters = ['All'] + sorted(df['Quarter-Year'].dropna().unique().tolist())
selected_quarter = st.sidebar.selectbox("Select Quarter", all_quarters)

all_weeks = ['All'] + sorted(df['Week Number'].dropna().unique().tolist())
selected_week = st.sidebar.selectbox("Select Week", all_weeks)

all_bins = ['All'] + sorted(df['Bin Category'].dropna().unique().tolist())
selected_bin = st.sidebar.selectbox("Select Bin", all_bins)

all_users = ['All'] + sorted(df['capstone_name'].dropna().unique().tolist())
selected_user = st.sidebar.selectbox("Select User Name", all_users)

# -------------------- Apply Filters --------------------
filtered_df = df.copy()
if selected_title != 'All':
    filtered_df = filtered_df[filtered_df['title'] == selected_title]
if selected_user != 'All':
    filtered_df = filtered_df[filtered_df['capstone_name'] == selected_user]
if selected_bin != 'All':
    filtered_df = filtered_df[filtered_df['Bin Category'] == selected_bin]
if selected_quarter != 'All':
    filtered_df = filtered_df[filtered_df['Quarter-Year'] == selected_quarter]
if selected_week != 'All':
    filtered_df = filtered_df[filtered_df['Week Number'] == selected_week]

# -------------------- KPI Calculation --------------------
unique_users = filtered_df['capstone_name'].nunique()
unique_dashboards = filtered_df[['Step 1', 'Step 2', 'Step 3']].nunique().sum()
total_transitions = len(filtered_df)
most_common_dashboard = filtered_df['Step 1'].mode().iloc[0].split('/')[-1] if not filtered_df.empty else "N/A"
most_active_user = filtered_df['capstone_name'].value_counts().idxmax() if not filtered_df.empty else "N/A"
avg_transitions = round(total_transitions / unique_users, 2) if unique_users > 0 else 0

# -------------------- KPI Display (3 per row, 2 rows) --------------------
# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='kpi-value'>{unique_users}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Unique Users</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-value'>{unique_dashboards}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Dashboards</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-value'>{total_transitions}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Transitions</div>", unsafe_allow_html=True)

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Row 2
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f"<div class='kpi-value'>{most_common_dashboard}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Top Dashboard</div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='kpi-value'>{most_active_user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Most Active User</div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='kpi-value'>{avg_transitions}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-label'>Avg/User</div>", unsafe_allow_html=True)

# -------------------- Top Dashboards Chart & Bin Chart Side-by-Side --------------------

#st.markdown("## Dashboard Usage Insights")

col1, col2 = st.columns(2)

# -------------------- Dashboard Usage Insights Section --------------------

col1, col2 = st.columns([1.2, 0.8])  # Shift first chart slightly left

# -------------------- Column 1: Top Dashboards Chart --------------------
with col1:
    # Dynamic title for dashboard chart
    if selected_title != 'All':
        st.markdown(f"""
        <div style="font-size:14px; margin-bottom:0.4rem;">
            <strong>Top 10 Accessed Dashboards for Role:</strong> <span style="color:#90cdf4; font-weight:600;">{selected_title}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:14px; margin-bottom:0.4rem;">
            <strong>Top 10 Accessed Dashboards for All Roles</strong>
        </div>
        """, unsafe_allow_html=True)

    step_counts = filtered_df['Step 1'].value_counts().head(10).reset_index()
    step_counts.columns = ['Full Path', 'Count']
    step_counts['Dashboard Label'] = step_counts['Full Path'].apply(lambda x: x.split('/')[-1])
    step_counts = step_counts[::-1].reset_index(drop=True)  # Reverse so biggest is on top

    fig_dash = px.bar(
        step_counts,
        x='Count',
        y='Dashboard Label',
        orientation='h',
        hover_data={'Full Path': True},
        text='Count',
        color_discrete_sequence=['#1a365d']
    )

    fig_dash.update_traces(
        textposition='outside',
        textfont_size=10,
        marker_line_width=0.4,
        marker_line_color='black',
        cliponaxis=False
    )

    fig_dash.update_layout(
        height=360,
        bargap=0.25,
        margin=dict(l=40, r=10, t=20, b=20),  # Shift left
        showlegend=False,
        font=dict(color='black', size=10),
        xaxis=dict(title="", tickfont=dict(color='black')),
        yaxis=dict(title="", tickfont=dict(color='black'), automargin=True)
    )

    st.plotly_chart(fig_dash, use_container_width=True)


# -------------------- Column 2: Bin Category Chart --------------------
with col2:
    # st.markdown("""
    # <div style="font-size:16px; font-weight:600; margin-bottom:0.4rem;">
    #     Bin Category Distribution by Role
    # </div>
    # """, unsafe_allow_html=True)

    if selected_title != 'All':
        st.markdown(f"""
        <div style="font-size:14px; margin-bottom:0.4rem;">
            <strong>Bin Category Distribution for Role:</strong> <span style="color:#90cdf4; font-weight:600;">{selected_title}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-size:14px; margin-bottom:0.4rem;">
            <strong>Bin Category Distribution for All Roles</strong>
        </div>
        """, unsafe_allow_html=True)

    bin_counts = filtered_df.groupby(['Bin Category']).size().reset_index(name='Count')
    bin_counts['Percentage'] = (bin_counts['Count'] / bin_counts['Count'].sum() * 100).round(2)
    bin_counts['Label'] = bin_counts.apply(lambda row: f"{row['Count']} ({row['Percentage']}%)", axis=1)
    bin_counts = bin_counts.sort_values(by="Count", ascending=False)

    pastel_colors_bin = ['#90cdf4', '#fef08a', '#1a365d', '#a7f3d0', '#fecaca']
    color_map_bin = {
        category: pastel_colors_bin[i % len(pastel_colors_bin)]
        for i, category in enumerate(bin_counts['Bin Category'])
    }

    fig_bin = px.bar(
        bin_counts,
        x='Bin Category',
        y='Count',
        text='Label',
        color='Bin Category',
        color_discrete_map=color_map_bin,
        hover_data={'Bin Category': True, 'Count': True, 'Percentage': True}
    )

    fig_bin.update_traces(
        textposition='outside',
        textfont_size=8,
        marker_line_color='black',
        marker_line_width=0.3,
        width=0.5,
        cliponaxis=False
    )

    fig_bin.update_layout(
        height=360,
        bargap=0.03,
        bargroupgap=0.01,
        margin=dict(l=5, r=5, t=20, b=10),
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        font=dict(color='black', size=9),
        xaxis=dict(titlefont=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(titlefont=dict(color='black'), tickfont=dict(color='black'))
    )

    st.plotly_chart(fig_bin, use_container_width=True)

# -------------------- Final Spacer --------------------
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

