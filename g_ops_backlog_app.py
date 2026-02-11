import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="G-Ops Backlog Tool",
    page_icon="📦",
    layout="wide"
)

# Google Sheet ID
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_dump_data():
    """Load data from Dump tab"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def filter_by_status(df, status):
    """Filter dataframe by latest_status"""
    if 'latest_status' not in df.columns:
        return pd.DataFrame()
    return df[df['latest_status'] == status].copy()

def filter_by_zone(df, zone_type):
    """Filter dataframe by QC or zone column"""
    if 'QC or zone' not in df.columns:
        return df
    if zone_type == "PK Zone":
        return df[df['QC or zone'] == 'PK Zone'].copy()
    elif zone_type == "QC Center":
        return df[df['QC or zone'] == 'PK QC Center'].copy()
    return df

def get_display_columns(order_type):
    """Get relevant columns for each order type"""
    base_cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 'vendor', 'total_order_line_amount']
    
    if order_type == 'approved':
        specific_cols = ['qc_approved_at', 'item_name', 'product_brand']
    elif order_type == 'handover':
        specific_cols = ['logistics_partner_handedover_at', 'logistics_partner_name', 'item_name']
    elif order_type == 'freight':
        specific_cols = ['freight_at', 'flight_number', 'logistics_partner_name', 'boxes']
    else:
        specific_cols = []
    
    return base_cols + specific_cols

def display_orders_table(df, order_type, search_term="", country_filter="All", zone_filter="All"):
    """Display filtered orders table"""
    if df.empty:
        st.info("No orders found.")
        return
    
    # Get relevant columns
    display_cols = get_display_columns(order_type)
    available_cols = [col for col in display_cols if col in df.columns]
    
    # Filter by zone first
    if zone_filter != "All":
        df = filter_by_zone(df, zone_filter)
    
    # Filter by search term
    if search_term:
        search_term = search_term.lower()
        mask = df.apply(lambda row: any(search_term in str(val).lower() for val in row), axis=1)
        df = df[mask]
    
    # Filter by country
    if country_filter != "All" and 'customer_country' in df.columns:
        df = df[df['customer_country'] == country_filter]
    
    if df.empty:
        st.info("No orders match your filters.")
        return
    
    # Display count
    st.write(f"**Showing {len(df)} orders**")
    
    # Display table
    display_df = df[available_cols].copy() if available_cols else df.copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{order_type}_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def main():
    st.title("📦 G-Ops Backlog Tool")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔄 Data Controls")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.header("🔍 Filters")
        
        # Search filter
        search_term = st.text_input("Search (Order #, Customer, Fleek ID)", "")
        
        # Load data for filters
        df = load_dump_data()
        
        # Country filter
        if not df.empty and 'customer_country' in df.columns:
            countries = ['All'] + sorted(df['customer_country'].dropna().unique().tolist())
            country_filter = st.selectbox("Filter by Country", countries)
        else:
            country_filter = "All"
        
        # Zone filter - NEW FILTER
        st.markdown("---")
        st.header("🏭 Zone Filter")
        zone_filter = st.radio(
            "Select Zone",
            ["All", "PK Zone", "QC Center"],
            help="Filter orders by PK Zone or QC Center"
        )
        
        st.markdown("---")
        st.header("📊 Order Counts")
        
        if not df.empty:
            # Status counts
            approved_count = len(df[df['latest_status'] == 'QC_APPROVED'])
            handover_count = len(df[df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER'])
            freight_count = len(df[df['latest_status'] == 'FREIGHT'])
            
            st.metric("QC Approved", approved_count)
            st.metric("Handed Over", handover_count)
            st.metric("Freight", freight_count)
            
            # Zone counts
            st.markdown("---")
            st.header("🏭 Zone Counts")
            if 'QC or zone' in df.columns:
                pk_zone_count = len(df[df['QC or zone'] == 'PK Zone'])
                qc_center_count = len(df[df['QC or zone'] == 'PK QC Center'])
                st.metric("PK Zone Orders", pk_zone_count)
                st.metric("QC Center Orders", qc_center_count)
    
    # Load data
    df = load_dump_data()
    
    if df.empty:
        st.error("Unable to load data. Please check the Google Sheet connection.")
        return
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["✅ QC Approved", "🚚 Handed Over", "✈️ Freight"])
    
    with tab1:
        st.header("QC Approved Orders")
        approved_df = filter_by_status(df, 'QC_APPROVED')
        
        # Show zone breakdown for this status
        if not approved_df.empty and 'QC or zone' in approved_df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                if zone_filter == "All":
                    st.info(f"📊 Total: {len(approved_df)}")
                else:
                    filtered_count = len(filter_by_zone(approved_df, zone_filter))
                    st.info(f"📊 Filtered ({zone_filter}): {filtered_count}")
            with col2:
                pk_zone = len(approved_df[approved_df['QC or zone'] == 'PK Zone'])
                st.info(f"🏭 PK Zone: {pk_zone}")
            with col3:
                qc_center = len(approved_df[approved_df['QC or zone'] == 'PK QC Center'])
                st.info(f"🏢 QC Center: {qc_center}")
        
        display_orders_table(approved_df, 'approved', search_term, country_filter, zone_filter)
    
    with tab2:
        st.header("Handed Over to Logistics Partner")
        handover_df = filter_by_status(df, 'HANDED_OVER_TO_LOGISTICS_PARTNER')
        
        # Show zone breakdown for this status
        if not handover_df.empty and 'QC or zone' in handover_df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                if zone_filter == "All":
                    st.info(f"📊 Total: {len(handover_df)}")
                else:
                    filtered_count = len(filter_by_zone(handover_df, zone_filter))
                    st.info(f"📊 Filtered ({zone_filter}): {filtered_count}")
            with col2:
                pk_zone = len(handover_df[handover_df['QC or zone'] == 'PK Zone'])
                st.info(f"🏭 PK Zone: {pk_zone}")
            with col3:
                qc_center = len(handover_df[handover_df['QC or zone'] == 'PK QC Center'])
                st.info(f"🏢 QC Center: {qc_center}")
        
        display_orders_table(handover_df, 'handover', search_term, country_filter, zone_filter)
    
    with tab3:
        st.header("Freight Orders")
        freight_df = filter_by_status(df, 'FREIGHT')
        
        # Show zone breakdown for this status
        if not freight_df.empty and 'QC or zone' in freight_df.columns:
            col1, col2, col3 = st.columns(3)
            with col1:
                if zone_filter == "All":
                    st.info(f"📊 Total: {len(freight_df)}")
                else:
                    filtered_count = len(filter_by_zone(freight_df, zone_filter))
                    st.info(f"📊 Filtered ({zone_filter}): {filtered_count}")
            with col2:
                pk_zone = len(freight_df[freight_df['QC or zone'] == 'PK Zone'])
                st.info(f"🏭 PK Zone: {pk_zone}")
            with col3:
                qc_center = len(freight_df[freight_df['QC or zone'] == 'PK QC Center'])
                st.info(f"🏢 QC Center: {qc_center}")
        
        display_orders_table(freight_df, 'freight', search_term, country_filter, zone_filter)
    
    # Footer
    st.markdown("---")
    st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data source: G-Ops Backlog Data tool")

if __name__ == "__main__":
    main()
