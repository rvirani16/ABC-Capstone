import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# -------------------- Page Setup --------------------
st.set_page_config(page_title="User Journey", layout="wide")
st.title("User Journey")

# -------------------- Custom CSS for KPIs --------------------
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
</style>
""", unsafe_allow_html=True)

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "..", "datasets", "user_level_with_names.csv")
    df = pd.read_csv(file_path)
    return df

df = load_data()

# -------------------- Preprocessing --------------------
for step in ['Step 1', 'Step 2', 'Step 3']:
    df[step + '_Clean'] = df[step].apply(lambda x: os.path.basename(str(x)) if pd.notnull(x) else "")

df['Parent Path'] = df['Step 1'].apply(lambda x: str(x).split('/')[2] if pd.notnull(x) and len(str(x).split('/')) > 2 else 'Other')

# -------------------- Always Available Download Button --------------------
st.markdown("### Download Full User Journey Data")
st.info("This download includes **all user journeys**, regardless of filters above.")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Full Dataset (CSV)",
    data=csv_data,
    file_name="full_user_journey.csv",
    mime="text/csv"
)

# -------------------- Sidebar Filters --------------------
st.sidebar.header("Filter Journey")

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

parent_paths = ['All'] + sorted(df['Parent Path'].dropna().unique().tolist())
selected_parent = st.sidebar.selectbox("Select Parent Path", parent_paths)

# -------------------- Apply Filters --------------------
filtered_df = df.copy()
if selected_title != 'All':
    filtered_df = filtered_df[filtered_df['title'] == selected_title]
if selected_quarter != 'All':
    filtered_df = filtered_df[filtered_df['Quarter-Year'] == selected_quarter]
if selected_week != 'All':
    filtered_df = filtered_df[filtered_df['Week Number'] == selected_week]
if selected_bin != 'All':
    filtered_df = filtered_df[filtered_df['Bin Category'] == selected_bin]
if selected_user != 'All':
    filtered_df = filtered_df[filtered_df['capstone_name'] == selected_user]
else:
    max_users = 5
    top_users = filtered_df['capstone_name'].value_counts().head(max_users).index.tolist()
    filtered_df = filtered_df[filtered_df['capstone_name'].isin(top_users)]
    st.info(f"Showing user journey for top {max_users} most active users.")

if selected_parent != 'All':
    filtered_df = filtered_df[filtered_df['Parent Path'] == selected_parent]

# -------------------- Conditional Rendering --------------------
if selected_title == 'All' or selected_quarter == 'All':
    st.warning("Please select a **Title** and **Quarter** to view the user journey.")
    st.stop()

# -------------------- Display KPI --------------------
unique_users = filtered_df['capstone_name'].nunique()
unique_dashboards = filtered_df[['Step 1', 'Step 2', 'Step 3']].nunique().sum()
total_transitions = len(filtered_df)
most_common_dashboard = filtered_df['Step 1'].mode().iloc[0].split('/')[-1] if not filtered_df.empty else "N/A"
most_active_user = filtered_df['capstone_name'].value_counts().idxmax() if not filtered_df.empty else "N/A"
avg_transitions = round(total_transitions / unique_users, 2) if unique_users > 0 else 0

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

st.markdown("<br>", unsafe_allow_html=True)

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

# -------------------- Journey Visualization --------------------
# -------------------- Journey Visualization --------------------
st.markdown("### Step-wise Journey Visualization")

color_map = {
    'Sales and GP': '#90cdf4',
    'Pricing Analytics': '#fde68a',
    'Inventory Insights': '#bbf7d0',
    'Operations Overview': '#fecaca',
    'Other': '#e2e8f0'
}
default_color = '#dbeafe'

grouped = filtered_df.groupby(['capstone_name', 'Week Number'])

for (user, week), group in grouped:
    st.markdown(f"**{user} | Week: {week}**")
    for _, row in group.iterrows():
        steps = [row['Step 1_Clean'], row['Step 2_Clean'], row['Step 3_Clean']]
        fig = go.Figure()
        x_pos = [0, 1.5, 3]  # Spread out for longer boxes

        for i, step in enumerate(steps):
            pastel_color = color_map.get(step, default_color)
            fig.add_shape(
                type="rect",
                x0=x_pos[i] - 0.5, y0=-0.2,
                x1=x_pos[i] + 0.5, y1=0.2,
                line=dict(color="rgba(0,0,0,0.1)", width=1),
                fillcolor=pastel_color,
                opacity=0.8,
                layer="below"
            )
            fig.add_trace(go.Scatter(
                x=[x_pos[i]], y=[0],
                mode="text",
                text=[step],
                textfont=dict(size=16, color="#333"),
                hoverinfo="text",
                showlegend=False
            ))

        for i in range(len(steps) - 1):
            fig.add_annotation(
                x=x_pos[i + 1] - 0.7, y=0,
                ax=x_pos[i] + 0.5, ay=0,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=0.7,
                arrowwidth=1.5,
                arrowcolor="gray"
            )

        fig.update_layout(
            height=150,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="white",
            hovermode="closest",
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
