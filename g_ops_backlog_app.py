
import streamlit as st
import pandas as pd

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

# Google Sheet ID
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name.replace(' ', '%20')}"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {e}")
        return pd.DataFrame()

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**📊 Data Source:**")
    st.markdown("Google Sheets + BigQuery")
    st.markdown("---")
    st.markdown(f"[📄 Open Sheet](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)")

# Load all data
df_approved = load_sheet_data("Approved Orders")
df_handover = load_sheet_data("Handover Orders")
df_freight = load_sheet_data("Freight Orders")

# Summary Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    total = len(df_approved) + len(df_handover) + len(df_freight)
    st.metric("📊 Total Orders", f"{total:,}")
with col2:
    st.metric("✅ Approved", f"{len(df_approved):,}")
with col3:
    st.metric("🚚 Handover", f"{len(df_handover):,}")
with col4:
    st.metric("📦 Freight", f"{len(df_freight):,}")

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["✅ Approved Orders", "🚚 Handover to Logistics", "📦 Freight Tracking"])

# Tab 1: Approved Orders
with tab1:
    st.subheader("✅ Approved Orders")
    
    if not df_approved.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Search Order/Customer", key="search_approved")
        with col2:
            if 'Current_Status' in df_approved.columns:
                status_options = df_approved['Current_Status'].dropna().unique().tolist()
                status_filter = st.multiselect("Status", status_options, key="status_approved")
        with col3:
            if 'Customer_Country' in df_approved.columns:
                country_options = df_approved['Customer_Country'].dropna().unique().tolist()
                country_filter = st.multiselect("Country", country_options, key="country_approved")
        
        # Apply Filters
        filtered = df_approved.copy()
        if search:
            filtered = filtered[
                filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            ]
        if 'status_filter' in dir() and status_filter:
            filtered = filtered[filtered['Current_Status'].isin(status_filter)]
        if 'country_filter' in dir() and country_filter:
            filtered = filtered[filtered['Customer_Country'].isin(country_filter)]
        
        st.dataframe(filtered, use_container_width=True, height=400)
        
        # Export
        csv = filtered.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, "approved_orders.csv", "text/csv")
    else:
        st.warning("No data available")

# Tab 2: Handover Orders
with tab2:
    st.subheader("🚚 Handover to Logistics")
    
    if not df_handover.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_h = st.text_input("🔍 Search Order/Customer", key="search_handover")
        with col2:
            if 'Current_Status' in df_handover.columns:
                status_options_h = df_handover['Current_Status'].dropna().unique().tolist()
                status_filter_h = st.multiselect("Status", status_options_h, key="status_handover")
        with col3:
            if 'Customer_Country' in df_handover.columns:
                country_options_h = df_handover['Customer_Country'].dropna().unique().tolist()
                country_filter_h = st.multiselect("Country", country_options_h, key="country_handover")
        
        # Apply Filters
        filtered_h = df_handover.copy()
        if search_h:
            filtered_h = filtered_h[
                filtered_h.astype(str).apply(lambda x: x.str.contains(search_h, case=False)).any(axis=1)
            ]
        if 'status_filter_h' in dir() and status_filter_h:
            filtered_h = filtered_h[filtered_h['Current_Status'].isin(status_filter_h)]
        if 'country_filter_h' in dir() and country_filter_h:
            filtered_h = filtered_h[filtered_h['Customer_Country'].isin(country_filter_h)]
        
        st.dataframe(filtered_h, use_container_width=True, height=400)
        
        csv_h = filtered_h.to_csv(index=False)
        st.download_button("📥 Download CSV", csv_h, "handover_orders.csv", "text/csv")
    else:
        st.warning("No data available")

# Tab 3: Freight Orders
with tab3:
    st.subheader("📦 Freight Tracking")
    
    if not df_freight.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_f = st.text_input("🔍 Search Order/Customer", key="search_freight")
        with col2:
            if 'Current_Status' in df_freight.columns:
                status_options_f = df_freight['Current_Status'].dropna().unique().tolist()
                status_filter_f = st.multiselect("Status", status_options_f, key="status_freight")
        with col3:
            if 'Customer_Country' in df_freight.columns:
                country_options_f = df_freight['Customer_Country'].dropna().unique().tolist()
                country_filter_f = st.multiselect("Country", country_options_f, key="country_freight")
        
        # Apply Filters
        filtered_f = df_freight.copy()
        if search_f:
            filtered_f = filtered_f[
                filtered_f.astype(str).apply(lambda x: x.str.contains(search_f, case=False)).any(axis=1)
            ]
        if 'status_filter_f' in dir() and status_filter_f:
            filtered_f = filtered_f[filtered_f['Current_Status'].isin(status_filter_f)]
        if 'country_filter_f' in dir() and country_filter_f:
            filtered_f = filtered_f[filtered_f['Customer_Country'].isin(country_filter_f)]
        
        st.dataframe(filtered_f, use_container_width=True, height=400)
        
        csv_f = filtered_f.to_csv(index=False)
        st.download_button("📥 Download CSV", csv_f, "freight_orders.csv", "text/csv")
    else:
        st.warning("No data available")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>G-Ops Backlog Tool | Built with ❤️ | Data: BigQuery via Google Sheets</p>
    </div>
    """, 
    unsafe_allow_html=True
)
