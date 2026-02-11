
import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import datetime

# Page Config
st.set_page_config(
    page_title="G-Ops Backlog",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">📦 G-Ops Backlog Tool</p>', unsafe_allow_html=True)

# BigQuery Connection
@st.cache_resource
def get_bigquery_client():
    # Option 1: Using service account JSON file
    # credentials = service_account.Credentials.from_service_account_file("your-service-account.json")
    # client = bigquery.Client(credentials=credentials, project="your-project-id")
    
    # Option 2: Using default credentials (when running on GCP or with gcloud auth)
    client = bigquery.Client()
    return client

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_approved_orders():
    client = get_bigquery_client()
    query = """
    SELECT 
        order_id as Order_ID,
        order_number as Order_Number,
        customer_name as Customer_Name,
        customer_country as Customer_Country,
        DATE(qc_approved_at) as Approval_Date,
        latest_status as Current_Status,
        logistics_partner_name as Logistics_Partner
    FROM `fleek_hub.order_line_details`
    WHERE qc_approved_at IS NOT NULL
    ORDER BY qc_approved_at DESC
    LIMIT 1000
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def load_handover_orders():
    client = get_bigquery_client()
    query = """
    SELECT 
        order_id as Order_ID,
        order_number as Order_Number,
        customer_name as Customer_Name,
        customer_country as Customer_Country,
        DATE(qc_approved_at) as Approval_Date,
        DATE(logistics_partner_handedover_at) as Handover_Date,
        logistics_partner_name as Logistics_Partner,
        latest_status as Current_Status
    FROM `fleek_hub.order_line_details`
    WHERE logistics_partner_handedover_at IS NOT NULL
    ORDER BY logistics_partner_handedover_at DESC
    LIMIT 1000
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def load_freight_orders():
    client = get_bigquery_client()
    query = """
    SELECT 
        order_id as Order_ID,
        order_number as Order_Number,
        customer_name as Customer_Name,
        customer_country as Customer_Country,
        DATE(qc_approved_at) as Approval_Date,
        DATE(logistics_partner_handedover_at) as Handover_Date,
        DATE(freight_at) as Freight_Date,
        DATE(freight_departed_at) as Freight_Departed_Date,
        logistics_partner_name as Logistics_Partner,
        latest_status as Current_Status
    FROM `fleek_hub.order_line_details`
    WHERE freight_at IS NOT NULL
    ORDER BY freight_at DESC
    LIMIT 1000
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def get_summary_stats():
    client = get_bigquery_client()
    query = """
    SELECT 
        COUNT(*) as total_orders,
        COUNT(CASE WHEN qc_approved_at IS NOT NULL THEN 1 END) as approved_orders,
        COUNT(CASE WHEN logistics_partner_handedover_at IS NOT NULL THEN 1 END) as handover_orders,
        COUNT(CASE WHEN freight_at IS NOT NULL THEN 1 END) as freight_orders,
        COUNT(CASE WHEN DATE(qc_approved_at) = CURRENT_DATE() THEN 1 END) as approved_today,
        COUNT(CASE WHEN DATE(logistics_partner_handedover_at) = CURRENT_DATE() THEN 1 END) as handover_today,
        COUNT(CASE WHEN DATE(freight_at) = CURRENT_DATE() THEN 1 END) as freight_today
    FROM `fleek_hub.order_line_details`
    """
    return client.query(query).to_dataframe()

# Sidebar - Refresh Button
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Last Updated:**")
    st.markdown(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load Summary Stats
try:
    stats = get_summary_stats()
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Orders", f"{stats['total_orders'].values[0]:,}")
    with col2:
        st.metric("✅ Approved", f"{stats['approved_orders'].values[0]:,}", f"+{stats['approved_today'].values[0]} today")
    with col3:
        st.metric("🚚 Handover", f"{stats['handover_orders'].values[0]:,}", f"+{stats['handover_today'].values[0]} today")
    with col4:
        st.metric("📦 Freight", f"{stats['freight_orders'].values[0]:,}", f"+{stats['freight_today'].values[0]} today")

except Exception as e:
    st.error(f"BigQuery Connection Error: {e}")
    st.info("Please check your BigQuery credentials")

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["✅ Approved Orders", "🚚 Handover to Logistics", "📦 Freight Tracking"])

# Tab 1: Approved Orders
with tab1:
    st.subheader("✅ Approved Orders")
    
    try:
        df_approved = load_approved_orders()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_approved = st.text_input("🔍 Search Order ID / Customer", key="search_approved")
        with col2:
            status_filter = st.multiselect("Status Filter", df_approved['Current_Status'].unique(), key="status_approved")
        with col3:
            partner_filter = st.multiselect("Logistics Partner", df_approved['Logistics_Partner'].dropna().unique(), key="partner_approved")
        
        # Apply Filters
        filtered_df = df_approved.copy()
        if search_approved:
            filtered_df = filtered_df[
                filtered_df['Order_ID'].astype(str).str.contains(search_approved, case=False) |
                filtered_df['Customer_Name'].astype(str).str.contains(search_approved, case=False)
            ]
        if status_filter:
            filtered_df = filtered_df[filtered_df['Current_Status'].isin(status_filter)]
        if partner_filter:
            filtered_df = filtered_df[filtered_df['Logistics_Partner'].isin(partner_filter)]
        
        # Display
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Export
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "approved_orders.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 2: Handover to Logistics
with tab2:
    st.subheader("🚚 Handover to Logistics")
    
    try:
        df_handover = load_handover_orders()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_handover = st.text_input("🔍 Search Order ID / Customer", key="search_handover")
        with col2:
            status_filter_h = st.multiselect("Status Filter", df_handover['Current_Status'].unique(), key="status_handover")
        with col3:
            partner_filter_h = st.multiselect("Logistics Partner", df_handover['Logistics_Partner'].dropna().unique(), key="partner_handover")
        
        # Apply Filters
        filtered_df_h = df_handover.copy()
        if search_handover:
            filtered_df_h = filtered_df_h[
                filtered_df_h['Order_ID'].astype(str).str.contains(search_handover, case=False) |
                filtered_df_h['Customer_Name'].astype(str).str.contains(search_handover, case=False)
            ]
        if status_filter_h:
            filtered_df_h = filtered_df_h[filtered_df_h['Current_Status'].isin(status_filter_h)]
        if partner_filter_h:
            filtered_df_h = filtered_df_h[filtered_df_h['Logistics_Partner'].isin(partner_filter_h)]
        
        # Display
        st.dataframe(filtered_df_h, use_container_width=True, height=400)
        
        # Export
        csv_h = filtered_df_h.to_csv(index=False)
        st.download_button("📥 Download CSV", csv_h, "handover_orders.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Tab 3: Freight Tracking
with tab3:
    st.subheader("📦 Freight Tracking")
    
    try:
        df_freight = load_freight_orders()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_freight = st.text_input("🔍 Search Order ID / Customer", key="search_freight")
        with col2:
            status_filter_f = st.multiselect("Status Filter", df_freight['Current_Status'].unique(), key="status_freight")
        with col3:
            partner_filter_f = st.multiselect("Logistics Partner", df_freight['Logistics_Partner'].dropna().unique(), key="partner_freight")
        
        # Apply Filters
        filtered_df_f = df_freight.copy()
        if search_freight:
            filtered_df_f = filtered_df_f[
                filtered_df_f['Order_ID'].astype(str).str.contains(search_freight, case=False) |
                filtered_df_f['Customer_Name'].astype(str).str.contains(search_freight, case=False)
            ]
        if status_filter_f:
            filtered_df_f = filtered_df_f[filtered_df_f['Current_Status'].isin(status_filter_f)]
        if partner_filter_f:
            filtered_df_f = filtered_df_f[filtered_df_f['Logistics_Partner'].isin(partner_filter_f)]
        
        # Display
        st.dataframe(filtered_df_f, use_container_width=True, height=400)
        
        # Export
        csv_f = filtered_df_f.to_csv(index=False)
        st.download_button("📥 Download CSV", csv_f, "freight_orders.csv", "text/csv")
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>G-Ops Backlog Tool | Built with ❤️ | Data Source: BigQuery</p>
    </div>
    """, 
    unsafe_allow_html=True
)
