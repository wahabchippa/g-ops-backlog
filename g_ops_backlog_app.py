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
def load_dump_data():
    """Load all data from Dump tab"""
    try:
        url = get_sheet_url("Dump")
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Dump data: {e}")
        return pd.DataFrame()

def filter_by_status(df, status):
    """Filter dataframe by latest_status"""
    if df.empty or 'latest_status' not in df.columns:
        return pd.DataFrame()
    return df[df['latest_status'] == status].copy()

def display_dataframe_with_filters(df, key_prefix):
    """Display dataframe with search and filters"""
    if df.empty:
        st.warning("No data available")
        return
    
    # Search box
    search_term = st.text_input("🔍 Search (Order Number, Customer Name, Fleek ID)", key=f"{key_prefix}_search")
    
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Orders", len(df))
    with col2:
        if 'customer_country' in df.columns:
            st.metric("🌍 Countries", df['customer_country'].nunique())
    with col3:
        if 'total_order_line_amount' in df.columns:
            total_value = df['total_order_line_amount'].astype(str).str.replace(',', '').astype(float).sum()
            st.metric("💰 Total Value", f"${total_value:,.2f}")
    
    # Select columns to display
    display_cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                    'total_order_line_amount', 'vendor', 'item_name', 'latest_status_date']
    
    # Filter to only existing columns
    display_cols = [col for col in display_cols if col in df.columns]
    
    # Add status-specific date columns
    if key_prefix == "approved" and 'qc_approved_at' in df.columns:
        display_cols.insert(4, 'qc_approved_at')
    elif key_prefix == "handover" and 'logistics_partner_handedover_at' in df.columns:
        display_cols.insert(4, 'logistics_partner_handedover_at')
        if 'logistics_partner_name' in df.columns:
            display_cols.insert(5, 'logistics_partner_name')
    elif key_prefix == "freight" and 'freight_at' in df.columns:
        display_cols.insert(4, 'freight_at')
        if 'logistics_partner_name' in df.columns:
            display_cols.insert(5, 'logistics_partner_name')
        if 'flight_number' in df.columns:
            display_cols.insert(6, 'flight_number')
    
    # Display dataframe with selected columns
    df_display = df[display_cols] if display_cols else df
    st.dataframe(df_display, use_container_width=True, height=400)
    
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

# Load all data from Dump
with st.spinner("Loading data from Dump..."):
    df_all = load_dump_data()

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Show summary counts
    st.header("📊 Current Status")
    if not df_all.empty and 'latest_status' in df_all.columns:
        approved_count = len(df_all[df_all['latest_status'] == 'QC_APPROVED'])
        handover_count = len(df_all[df_all['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER'])
        freight_count = len(df_all[df_all['latest_status'] == 'FREIGHT'])
        
        st.metric("📦 Approved", approved_count)
        st.metric("🚚 Handover", handover_count)
        st.metric("✈️ Freight", freight_count)
    
    st.divider()
    st.caption("Last Updated:")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.divider()
    st.caption("Data Source: Google Sheets (Dump)")
    st.caption(f"[View Sheet](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit)")

# Tabs
tab1, tab2, tab3 = st.tabs(["📦 Approved Orders", "🚚 Handover Orders", "✈️ Freight Orders"])

with tab1:
    st.header("📦 Approved Orders")
    st.caption("Orders with status: QC_APPROVED")
    df_approved = filter_by_status(df_all, 'QC_APPROVED')
    display_dataframe_with_filters(df_approved, "approved")

with tab2:
    st.header("🚚 Handover Orders")
    st.caption("Orders with status: HANDED_OVER_TO_LOGISTICS_PARTNER")
    df_handover = filter_by_status(df_all, 'HANDED_OVER_TO_LOGISTICS_PARTNER')
    display_dataframe_with_filters(df_handover, "handover")

with tab3:
    st.header("✈️ Freight Orders")
    st.caption("Orders with status: FREIGHT")
    df_freight = filter_by_status(df_all, 'FREIGHT')
    display_dataframe_with_filters(df_freight, "freight")

# Footer
st.divider()
st.caption("G-Ops Backlog Tool | Data auto-filters from Dump tab by latest_status | Click 'Refresh Data' for latest")
