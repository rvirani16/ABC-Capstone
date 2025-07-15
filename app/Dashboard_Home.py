import streamlit as st

# Set page config to make it wider
st.set_page_config(
    page_title="Dashboard Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling with light theme
st.markdown("""
<style>
    .dashboard-tile {
        background-color: #90cdf4;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        border: 1px solid #90cdf4;
    }
    .dashboard-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .kpi-container {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
    }
    .kpi-box {
        background-color: #90cdf4;
        border-radius: 5px;
        padding: 10px;
        width: 48%;
        text-align: center;
        border: 1px solid #90cdf4;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: bold;
        color: #1a365d;
    }
    .kpi-label {
        font-size: 20px;
        color: #4a5568;
    }
    h3 {
        color: #2d3748;
    }
    .dashboard-tile h3 {
        color: #2d3748 !important;
    }
</style>
""", unsafe_allow_html=True)


st.title("Dashboard Home")
st.markdown("##### Select a dashboard to view detailed metrics")

def dashboard_tile(title, kpi1_label, kpi1_value, kpi2_label, kpi2_value, dashboard_url):
    html = f"""
    <a href="{dashboard_url}" target="_self" style="text-decoration: none;">
        <div class="dashboard-tile">
            <h3>{title}</h3>
            <div class="kpi-container">
                <div class="kpi-box">
                    <div class="kpi-value">{kpi1_value}</div>
                    <div class="kpi-label">{kpi1_label}</div>
                </div>
                <div class="kpi-box">
                    <div class="kpi-value">{kpi2_value}</div>
                    <div class="kpi-label">{kpi2_label}</div>
                </div>
            </div>
        </div>
    </a>
    """
    return html

# Create a 2x2 grid for dashboard tiles
col1, col2 = st.columns(2)

with col1:
    # Dashboard 1
    st.markdown(
        dashboard_tile(
            "Notification Tracking",
            "Sent",
            "377K",
            "Viewed",
            "18K",
            "./Sent_Notification"
        ),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard 2
    st.markdown(
        dashboard_tile(
            "Error Analysis",
            "Total Errors",
            "5K",
            "Affected Dashboards",
            "265",
            "./Errors"
        ),
        unsafe_allow_html=True
    )

with col2:
    # Dashboard 3
    st.markdown(
        dashboard_tile(
            "Report Usage",
            "Reports Accessed",
            "7K",
            "QoQ Views",
            "179K",
            "./Dashboard_Trends"
        ),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard 4
    st.markdown(
        dashboard_tile(
            "User Journey Mapping",
            "Unique Users",
            "633",
            "Dashboards",
            "396",
            "./User_Journey_Mapping"
        ),
        unsafe_allow_html=True
    )