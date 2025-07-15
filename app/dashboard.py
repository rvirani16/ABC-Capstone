# Full enhanced Streamlit app code for ABC Supply
 
import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
from datetime import date
 
# Set layout and inject CSS
st.set_page_config(page_title="ABC App", layout="wide")
 
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #f8fbff;
            font-family: 'Segoe UI', sans-serif;
            font-size: 18px;
        }
        h1, h2, h3, h4 {
            color: #004080;
            font-size: 32px !important;
        }
        .abc-header h1 {
            font-size: 42px !important;
        }
        .abc-header p {
            font-size: 20px;
        }
        .info-box {
            background-color: #dbeaff;
            padding: 12px 18px;
            border-left: 6px solid #004080;
            margin-bottom: 20px;
            border-radius: 6px;
            font-size: 18px;
        }
        [data-testid="stSidebar"] {
            background-color: #e6f0ff;
            font-size: 18px;
        }
        .stSelectbox > div, .stRadio > div, .stDateInput > div, .stButton > button {
            font-size: 18px !important;
        }
        .stMetric label {
            font-size: 20px !important;
        }
        .stMetric div {
            font-size: 26px !important;
        }
        .css-1v0mbdj p {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)
 
# SQL CONNECTIONS
@st.cache_data(show_spinner=False)
def get_hierarchy_from_sql():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-41TELJC\SQLEXPRESS;'
        r'DATABASE=ABC_Supply;'
        r'Trusted_Connection=yes;'
    )
    query = "SELECT capstone_ad_account, capstone_name, H1, H2, H3, H4, H5, H6, H7, H8, H9 FROM Hierarchy_new"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
 
@st.cache_data(show_spinner=False)
def get_activity_data(source):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=DESKTOP-41TELJC\SQLEXPRESS;'
        r'DATABASE=ABC_Supply;'
        r'Trusted_Connection=yes;'
    )
    if source == "Tableau":
        query = """
        SELECT DISTINCT Tableau_Project, Tableau_Workbook, Tableau_Dashboard,
               FORMAT(TRY_CONVERT(DATETIME, Tableau_CreatedAt, 105), 'yyyy-MM-dd') AS Tableau_CreatedAt,
               Tableau_DayofWeek, Tableau_Username, Tableau_DisplayName,
               Tableau_Title, Tableau_Roles, Tableau_Email
        FROM tableau_logs_streamlit_final
        """
    else:
        query = """
        SELECT DISTINCT
               FORMAT(CAST(Oracle_StartTimestamp AS datetime), 'yyyy-MM-dd') AS Oracle_StartTimestamp,
               Oracle_SubjectArea,
               Oracle_DashboardName,
               Oracle_DashboardPage,
               Oracle_QuerySourceCode,
               Oracle_PresentationName,
               UPPER(Oracle_ID) AS Oracle_ID,
               Oracle_Email,
               Oracle_Role,
               Oracle_Name
        FROM dbo.oraclesqlfinal
        WHERE Oracle_ID NOT IN ('SA-OACProd')
        """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
 
def login(hierarchy_df):
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
 
    if not st.session_state.logged_in:
        # Show ABC branding ONLY during login
        st.markdown("""
            <div class='abc-header'>
                <h1>ABC Supply – Data Insights Dashboard</h1>
                <p style="margin-top:-10px;">Visualizing Tableau & Oracle activity by hierarchy, name, role, and date.</p>
            </div>
        """, unsafe_allow_html=True)
 
        st.markdown("""
            <div class='info-box'>
                📌 Use the sidebar to filter data by hierarchy, name, role, and date. Results will update in real time.
            </div>
        """, unsafe_allow_html=True)
 
        st.title("🔐 Login Page")
        login_account = st.text_input("Enter User ID")
        password = st.text_input("Enter Password", type="password")
 
        if st.button("Login"):
            matching_user = hierarchy_df[hierarchy_df['capstone_ad_account'] == login_account]
            if password == "streamlit123" and not matching_user.empty:
                st.session_state.logged_in = True
                st.session_state.login_name = matching_user.iloc[0]['capstone_name'].strip().lower()
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
 
        st.stop()
 
    return st.session_state.login_name
# App start
hierarchy_df = get_hierarchy_from_sql()
login_name = login(hierarchy_df)
 
st.sidebar.markdown(f"👤 **Logged in as:** `{st.session_state.login_name.title()}`")
# Sidebar filters
st.sidebar.markdown("### 📊 Dashboard")
data_source = st.sidebar.radio("", ["Tableau", "Oracle"], horizontal=True)
activity_df = get_activity_data(data_source)
 
labels = {
    "Tableau": {
        "dashboard_title": "📊 Dashboard Overview – Tableau",
        "kpi_labels": ["Workbooks", "Views", "Projects"],
        "chart_title_prefix": "Top 5",
        "role_occurrence_title": "📊 Role Occurrence (Tableau)"
    },
    "Oracle": {
        "dashboard_title": "📊 Dashboard Overview – Oracle",
        "kpi_labels": ["Dashboards", "Pages", "Subject Areas"],
        "chart_title_prefix": "Top 5",
        "role_occurrence_title": "📊 Role Occurrence (Oracle)"
    }
}
 
# Column setup
if data_source == "Tableau":
    display_col = 'Tableau_DisplayName'
    role_col = 'Tableau_Roles'
    date_col = 'Tableau_CreatedAt'
    project_col = 'Tableau_Project'
    workbook_col = 'Tableau_Workbook'
    dashboard_col = 'Tableau_Dashboard'
else:
    display_col = 'Oracle_Name'
    role_col = 'Oracle_Role'
    date_col = 'Oracle_StartTimestamp'
    project_col = 'Oracle_SubjectArea'
    workbook_col = 'Oracle_DashboardName'
    dashboard_col = 'Oracle_DashboardPage'
 
activity_df[display_col] = activity_df[display_col].astype(str).str.strip().str.lower()
activity_df[role_col] = activity_df[role_col].astype(str).str.strip().str.lower()
 
st.sidebar.markdown("### 🧭 Hierarchy")
user_tree = hierarchy_df[hierarchy_df['H1'].str.strip().str.lower() == login_name].copy()
selected_path = {}
 
for i in range(2, 10):
    col = f'H{i}'
    label = f"Hierarchy {i}"
    temp_tree = user_tree.copy()
    for level, val in selected_path.items():
        temp_tree = temp_tree[temp_tree[level] == val]
    options = sorted(temp_tree[col].dropna().unique())
    if not options:
        break
    selected_val = st.sidebar.selectbox(label, ["None"] + [str(opt) for opt in options], key=col)
    if selected_val != "None":
        selected_path[col] = selected_val
        user_tree = temp_tree[temp_tree[col] == selected_val]
    else:
        break
 
descendant_names = set()
for col in user_tree.columns[3:]:
    descendant_names.update(user_tree[col].dropna().unique())
descendant_names = {name.strip().lower() for name in descendant_names if isinstance(name, str) and name.strip()}
activity_df = activity_df[activity_df[display_col].isin(descendant_names)]
 
# Name and role filters
st.sidebar.markdown("### 👤 Name")
users = sorted(activity_df[display_col].dropna().unique())
selected_user = st.sidebar.selectbox("Display Name", ["All"] + users)
 
roles = activity_df[role_col].dropna()
roles = roles[~roles.isin(["0", "null", "", "none", "nan"])]
roles = sorted(roles.unique())
selected_role = st.sidebar.selectbox("🎭 Role", ["All"] + roles)
 
# Date filtering
activity_df[date_col] = pd.to_datetime(activity_df[date_col], errors='coerce')
activity_df = activity_df[~activity_df[date_col].isna()]
min_date = activity_df[date_col].min()
max_date = activity_df[date_col].max()
today = date.today()
if pd.isna(min_date): min_date = today
if pd.isna(max_date): max_date = today
if isinstance(min_date, pd.Timestamp): min_date = min_date.date()
if isinstance(max_date, pd.Timestamp): max_date = max_date.date()
date_range = st.sidebar.date_input("🗕️ Date Range", value=(min_date, max_date))
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Please select a valid start and end date.")
    st.stop()
if st.sidebar.button("🚪 Log Out"):
    st.session_state.logged_in = False
    st.rerun()
 
# Apply filters
activity_df_unfiltered_roles = activity_df.copy()
if selected_user != "All":
    activity_df = activity_df[activity_df[display_col] == selected_user]
if selected_role != "All":
    activity_df = activity_df[activity_df[role_col] == selected_role]
activity_df = activity_df[
    (activity_df[date_col] >= pd.to_datetime(start_date)) &
    (activity_df[date_col] <= pd.to_datetime(end_date))
]
if activity_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()
 
# KPI dashboard
# st.markdown(f"## {labels[data_source]['dashboard_title']}")
# if data_source == "Oracle":
#     kpi1, kpi2, kpi3, kpi4 = st.columns(4)
#     kpi_names = labels[data_source]['kpi_labels'] + ["Presentation Names"]
# else:
#     kpi1, kpi2, kpi3 = st.columns(3)
#     kpi_names = labels[data_source]['kpi_labels']
# if "kpi_choice" not in st.session_state:
#     st.session_state.kpi_choice = kpi_names[0]
 
# with kpi1:
#     if st.button(f"📘 {kpi_names[0]}"):
#         st.session_state.kpi_choice = kpi_names[0]
#     value = activity_df[workbook_col].dropna().nunique()
#     st.metric(label=kpi_names[0], value=value)
# with kpi2:
#     if st.button(f"👁️ {kpi_names[1]}"):
#         st.session_state.kpi_choice = kpi_names[1]
#     value = activity_df[dashboard_col].dropna().nunique()
#     st.metric(label=kpi_names[1], value=value)
# with kpi3:
#     if st.button(f"📁 {kpi_names[2]}"):
#         st.session_state.kpi_choice = kpi_names[2]
#     value = activity_df[project_col].dropna().nunique()
#     st.metric(label=kpi_names[2], value=value)
# if data_source == "Oracle":
#     with kpi4:
#         if st.button(f"🎤 {kpi_names[3]}"):
#             st.session_state.kpi_choice = kpi_names[3]
#         value = activity_df['Oracle_PresentationName'].dropna().nunique()
#         st.metric(label=kpi_names[3], value=value)
 
# # Charts
# col1, col2 = st.columns(2)
# with col1:
#     st.subheader(f"📈 {labels[data_source]['chart_title_prefix']} {st.session_state.kpi_choice}")
#     if st.session_state.kpi_choice == kpi_names[0]:
#         top5_df = activity_df[workbook_col].value_counts().nlargest(5).reset_index()
#     elif st.session_state.kpi_choice == kpi_names[1]:
#         top5_df = activity_df[dashboard_col].value_counts().nlargest(5).reset_index()
#     elif st.session_state.kpi_choice == kpi_names[2]:
#         top5_df = activity_df[project_col].value_counts().nlargest(5).reset_index()
#     elif data_source == "Oracle" and st.session_state.kpi_choice == kpi_names[3]:
#         top5_df = activity_df['Oracle_PresentationName'].value_counts().nlargest(5).reset_index()
#     else:
#         top5_df = pd.DataFrame(columns=['Label', 'Count'])
#     top5_df.columns = ['Label', 'Count']
#     fig = px.pie(top5_df, names='Label', values='Count', hole=0.4)
#     st.plotly_chart(fig, use_container_width=True, key="top5_kpi_chart")
# with col2:
#     st.subheader(labels[data_source]['role_occurrence_title'])
#     cleaned_roles = activity_df_unfiltered_roles[role_col].astype(str).str.strip().str.lower()
#     cleaned_roles = cleaned_roles[~cleaned_roles.isin(["", "0", "null", "none", "nan"])]
#     role_counts = cleaned_roles.value_counts().reset_index()
#     role_counts.columns = ['Role', 'Count']
#     total_roles = role_counts['Count'].sum()
#     role_counts['Role Occurrence %'] = (role_counts['Count'] / total_roles * 100).round(2)
#     fig_role = px.bar(role_counts.head(5), x='Role', y='Role Occurrence %', text='Role Occurrence %')
#     st.plotly_chart(fig_role, use_container_width=True, key="role_occurrence_chart")
 
# # Raw data
# with st.expander("🧾 View Raw Data Table"):
#     st.dataframe(activity_df)
 
st.sidebar.markdown("### 🔁 View Toggle")
show_paths = st.sidebar.checkbox("Show Navigation Paths Instead")
 
# --- Render either Navigation Paths or KPI Dashboard ---
if show_paths:
    st.subheader("🧭 Top 5 Navigation Paths")
    if data_source == "Tableau":
        activity_df['Navigation Path'] = (
            activity_df['Tableau_Project'].fillna('Unknown') + " → " +
            activity_df['Tableau_Workbook'].fillna('Unknown') + " → " +
            activity_df['Tableau_Dashboard'].fillna('Unknown')
        )
        path_group = ['Tableau_Project', 'Tableau_Workbook', 'Tableau_Dashboard']
    else:
        activity_df['Navigation Path'] = (
            activity_df['Oracle_PresentationName'].fillna('Unknown') + " → " +
            activity_df['Oracle_DashboardName'].fillna('Unknown') + " → " +
            activity_df['Oracle_DashboardPage'].fillna('Unknown')
        )
        path_group = ['Oracle_PresentationName', 'Oracle_DashboardName', 'Oracle_DashboardPage']
 
    path_df = (
        activity_df.groupby(path_group)
        .size()
        .reset_index(name='Count')
        .sort_values(by='Count', ascending=False)
        .head(5)
    )
 
    for i, row in path_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([4, 0.5, 4, 0.5, 4, 1])
        with col1:
            st.markdown(f"<div style='background-color:#e0f7fa;padding:10px;border-radius:10px;text-align:center;'><b>{row[path_group[0]]}</b></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='text-align:center;font-size:24px;'>→</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='background-color:#f1f8e9;padding:10px;border-radius:10px;text-align:center;'><b>{row[path_group[1]]}</b></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div style='text-align:center;font-size:24px;'>→</div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div style='background-color:#fff3e0;padding:10px;border-radius:10px;text-align:center;'><b>{row[path_group[2]]}</b></div>", unsafe_allow_html=True)
        with col6:
            st.markdown(f"<div style='text-align:center; font-size:14px; margin-top:10px;'><b>Count: {row['Count']}</b></div>", unsafe_allow_html=True)
        st.markdown("---")
else:
    # KPI Dashboard section
    st.markdown(f"## {labels[data_source]['dashboard_title']}")
    if data_source == "Oracle":
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi_names = labels[data_source]['kpi_labels'] + ["Presentation Names"]
    else:
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi_names = labels[data_source]['kpi_labels']
    if "kpi_choice" not in st.session_state:
        st.session_state.kpi_choice = kpi_names[0]
 
    with kpi1:
        if st.button(f"📘 {kpi_names[0]}", key="kpi_btn_1"):
            st.session_state.kpi_choice = kpi_names[0]
        value = activity_df[workbook_col].dropna().nunique()
        st.metric(label=kpi_names[0], value=value)
    with kpi2:
        if st.button(f"👁️ {kpi_names[1]}", key="kpi_btn_2"):
            st.session_state.kpi_choice = kpi_names[1]
        value = activity_df[dashboard_col].dropna().nunique()
        st.metric(label=kpi_names[1], value=value)
    with kpi3:
        if st.button(f"📁 {kpi_names[2]}", key="kpi_btn_3"):
            st.session_state.kpi_choice = kpi_names[2]
        value = activity_df[project_col].dropna().nunique()
        st.metric(label=kpi_names[2], value=value)
    if data_source == "Oracle":
        with kpi4:
            if st.button(f"🎤 {kpi_names[3]}", key="kpi_btn_4"):
                st.session_state.kpi_choice = kpi_names[3]
            value = activity_df['Oracle_PresentationName'].dropna().nunique()
            st.metric(label=kpi_names[3], value=value)
 
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📈 {labels[data_source]['chart_title_prefix']} {st.session_state.kpi_choice}")
        if st.session_state.kpi_choice == kpi_names[0]:
            top5_df = activity_df[workbook_col].value_counts().nlargest(5).reset_index()
        elif st.session_state.kpi_choice == kpi_names[1]:
            top5_df = activity_df[dashboard_col].value_counts().nlargest(5).reset_index()
        elif st.session_state.kpi_choice == kpi_names[2]:
            top5_df = activity_df[project_col].value_counts().nlargest(5).reset_index()
        elif data_source == "Oracle" and st.session_state.kpi_choice == kpi_names[3]:
            top5_df = activity_df['Oracle_PresentationName'].value_counts().nlargest(5).reset_index()
        else:
            top5_df = pd.DataFrame(columns=['Label', 'Count'])
        top5_df.columns = ['Label', 'Count']
        fig = px.pie(top5_df, names='Label', values='Count', hole=0.4)
        st.plotly_chart(fig, use_container_width=True, key="top5_kpi_chart_toggle")
    with col2:
        st.subheader(labels[data_source]['role_occurrence_title'])
        cleaned_roles = activity_df_unfiltered_roles[role_col].astype(str).str.strip().str.lower()
        cleaned_roles = cleaned_roles[~cleaned_roles.isin(["", "0", "null", "none", "nan"])]
        role_counts = cleaned_roles.value_counts().reset_index()
        role_counts.columns = ['Role', 'Count']
        total_roles = role_counts['Count'].sum()
        role_counts['Role Occurrence %'] = (role_counts['Count'] / total_roles * 100).round(2)
        fig_role = px.bar(role_counts.head(5), x='Role', y='Role Occurrence %', text='Role Occurrence %')
        st.plotly_chart(fig_role, use_container_width=True, key="role_occurrence_chart_toggle")
 
    # Raw data
    with st.expander("🧾 View Raw Data Table"):
        st.dataframe(activity_df)
 