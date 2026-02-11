import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="G-Ops Backlog Tool",
    page_icon="📦",
    layout="wide"
)

# Google Sheet ID
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

def get_sheet_url(sheet_name):
    """Generate CSV export URL for a Google Sheet tab"""
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name.replace(' ', '%20')}"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_approved_orders():
    """Load Approved Orders from Google Sheet"""
    try:
        url = get_sheet_url("Approved Orders")
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Approved Orders: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_handover_orders():
    """Load Handover Orders from Google Sheet"""
    try:
        url = get_sheet_url("Handover Orders")
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Handover Orders: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_freight_orders():
    """Load Freight Orders from Google Sheet"""
    try:
        url = get_sheet_url("Freight Orders")
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Freight Orders: {e}")
        return pd.DataFrame()

def display_dataframe_with_filters(df, key_prefix):
    """Display dataframe with search and filters"""
    if df.empty:
        st.warning("No data available")
        return
    
    # Search box
    search_term = st.text_input("🔍 Search (Order ID, Customer Name, Email)", key=f"{key_prefix}_search")
    
    # Apply search filter
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        df = df[mask]
    
    # Country filter if column exists
    if 'customer_country' in df.columns:
        countries = ['All'] + sorted(df['customer_country'].dropna().unique().tolist())
        selected_country = st.selectbox("🌍 Filter by Country", countries, key=f"{key_prefix}_country")
        if selected_country != 'All':
            df = df[df['customer_country'] == selected_country]
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Orders", len(df))
    with col2:
        if 'customer_country' in df.columns:
            st.metric("Countries", df['customer_country'].nunique())
    
    # Display dataframe
    st.dataframe(df, use_container_width=True, height=400)
    
    # Export button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{key_prefix}_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        key=f"{key_prefix}_download"
    )

# Main app
st.title("📦 G-Ops Backlog Tool")

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.caption("Last Updated:")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.divider()
    st.caption("Data Source: Google Sheets")
    st.caption(f"[View Sheet](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)")

# Tabs
tab1, tab2, tab3 = st.tabs(["✅ Approved Orders", "🚚 Handover to Logistics", "📦 Freight Tracking"])

with tab1:
    st.header("✅ Approved Orders")
    st.caption("Orders that are QC approved but not yet handed over to logistics")
    df_approved = load_approved_orders()
    display_dataframe_with_filters(df_approved, "approved")

with tab2:
    st.header("🚚 Handover to Logistics")
    st.caption("Orders handed over to logistics partner but not yet in freight")
    df_handover = load_handover_orders()
    display_dataframe_with_filters(df_handover, "handover")

with tab3:
    st.header("📦 Freight Tracking")
    st.caption("Orders currently in freight/transit")
    df_freight = load_freight_orders()
    display_dataframe_with_filters(df_freight, "freight")

# Footer
st.divider()
st.caption("G-Ops Backlog Tool | Data refreshes every 5 minutes | Click 'Refresh Data' for latest")
