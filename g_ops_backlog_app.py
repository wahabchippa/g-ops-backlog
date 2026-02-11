import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="G-Ops Backlog Tool",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main page styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        color: #b8d4e8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Clickable metric cards */
    .clickable-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #2d5a87;
        transition: all 0.3s;
        cursor: pointer;
        margin-bottom: 1rem;
        text-align: center;
    }
    .clickable-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .clickable-card h3 {
        color: #1e3a5f;
        font-size: 1rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .clickable-card .value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .clickable-card .subtitle {
        color: #666;
        font-size: 0.85rem;
    }
    
    /* Card colors */
    .card-green { border-left-color: #28a745; }
    .card-green .value { color: #28a745; }
    
    .card-blue { border-left-color: #17a2b8; }
    .card-blue .value { color: #17a2b8; }
    
    .card-yellow { border-left-color: #ffc107; }
    .card-yellow .value { color: #ffc107; }
    
    .card-red { border-left-color: #dc3545; }
    .card-red .value { color: #dc3545; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2d5a87 100%);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    [data-testid="stSidebar"] p {
        color: #b8d4e8 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2d5a87 0%, #1e3a5f 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .page-header h2 {
        margin: 0;
        font-size: 1.8rem;
    }
    .page-header p {
        margin: 0.5rem 0 0 0;
        color: #b8d4e8;
    }
    
    /* Section titles */
    .section-title {
        color: #1e3a5f;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Google Sheet ID
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_dump_data():
    """Load data from Dump tab"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_display_columns():
    """Get columns to display in tables"""
    return ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
            'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at', 
            'product_brand', 'QC or zone', 'Order Type']

def display_orders_page(df, title, subtitle, color_class):
    """Display orders in a professional table format"""
    
    # Header
    st.markdown(f"""
    <div class="page-header">
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No orders found.")
        return
    
    # Filters row
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search by Order #, Customer, Fleek ID", "", key=f"search_{title}")
    with col2:
        if 'customer_country' in df.columns:
            countries = ['All Countries'] + sorted(df['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries, key=f"country_{title}")
        else:
            country = "All Countries"
    with col3:
        st.write("")
        st.write("")
        csv = df.to_csv(index=False)
        st.download_button("📥 Export CSV", csv, f"{title.lower().replace(' ', '_')}.csv", "text/csv", key=f"csv_{title}")
    
    # Apply filters
    filtered_df = df.copy()
    if search:
        search = search.lower()
        mask = filtered_df.apply(lambda row: any(search in str(val).lower() for val in row), axis=1)
        filtered_df = filtered_df[mask]
    
    if country != "All Countries" and 'customer_country' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['customer_country'] == country]
    
    # Get display columns
    display_cols = get_display_columns()
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    # Stats row
    st.markdown(f"**📊 Showing {len(filtered_df):,} orders**")
    
    # Display table
    if not filtered_df.empty:
        display_df = filtered_df[available_cols].copy() if available_cols else filtered_df.copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    else:
        st.warning("No orders match your filters.")

def main():
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    
    # Load data
    df = load_dump_data()
    
    if df.empty:
        st.error("Unable to load data. Please check connection.")
        return
    
    # Filter: QC_APPROVED only
    approved_df = df[df['latest_status'] == 'QC_APPROVED'].copy() if 'latest_status' in df.columns else pd.DataFrame()
    
    # PK Zone - NORMAL ORDERS ONLY (QC Approved)
    pk_zone_normal = approved_df[
        (approved_df['QC or zone'] == 'PK Zone') & 
        (approved_df['Order Type'] == 'Normal Order')
    ] if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns else pd.DataFrame()
    
    # QC Center - NORMAL ORDERS ONLY (QC Approved)
    qc_center_normal = approved_df[
        (approved_df['QC or zone'] == 'PK QC Center') & 
        (approved_df['Order Type'] == 'Normal Order')
    ] if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns else pd.DataFrame()
    
    # AI Orders - PK Zone (QC Approved)
    ai_pk_zone = approved_df[
        (approved_df['QC or zone'] == 'PK Zone') & 
        (approved_df['Order Type'] == 'AI Order')
    ] if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns else pd.DataFrame()
    
    # AI Orders - QC Center (QC Approved)
    ai_qc_center = approved_df[
        (approved_df['QC or zone'] == 'PK QC Center') & 
        (approved_df['Order Type'] == 'AI Order')
    ] if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns else pd.DataFrame()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <h1 style="color: white; font-size: 1.6rem; margin: 0;">📦 G-Ops Backlog</h1>
            <p style="color: #b8d4e8; font-size: 0.85rem; margin-top: 0.3rem;">Operations Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Dashboard button
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 0.5rem;">
            <p style="margin: 0.3rem 0;"><strong>🟢 PK Zone:</strong> {len(pk_zone_normal):,}</p>
            <p style="margin: 0.3rem 0;"><strong>🔵 QC Center:</strong> {len(qc_center_normal):,}</p>
            <p style="margin: 0.3rem 0;"><strong>🟡 AI Zone:</strong> {len(ai_pk_zone):,}</p>
            <p style="margin: 0.3rem 0;"><strong>🔴 AI QC:</strong> {len(ai_qc_center):,}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem 0;">
            <p style="color: #b8d4e8; font-size: 0.7rem;">
                Last Updated<br>
                {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on current view
    if st.session_state.current_view == 'dashboard':
        # Dashboard Header
        st.markdown("""
        <div class="main-header">
            <h1>📦 G-Ops Backlog Dashboard</h1>
            <p>Real-time Operations Tracking & Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Normal Orders Section
        st.markdown('<div class="section-title">🏭 Approved Orders (Normal Orders Only)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🟢 PK Zone

{len(pk_zone_normal):,} Orders", key="btn_pk_zone", use_container_width=True):
                st.session_state.current_view = 'pk_zone'
                st.rerun()
            st.markdown(f"""
            <div class="clickable-card card-green" onclick="document.querySelector('[data-testid=\"btn_pk_zone\"]').click()">
                <h3>🟢 PK Zone</h3>
                <div class="value">{len(pk_zone_normal):,}</div>
                <div class="subtitle">Normal Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"🔵 QC Center

{len(qc_center_normal):,} Orders", key="btn_qc_center", use_container_width=True):
                st.session_state.current_view = 'qc_center'
                st.rerun()
            st.markdown(f"""
            <div class="clickable-card card-blue">
                <h3>🔵 QC Center</h3>
                <div class="value">{len(qc_center_normal):,}</div>
                <div class="subtitle">Normal Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # AI Orders Section
        st.markdown('<div class="section-title">🤖 AI Orders (Approved)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🟡 AI PK Zone

{len(ai_pk_zone):,} Orders", key="btn_ai_zone", use_container_width=True):
                st.session_state.current_view = 'ai_pk_zone'
                st.rerun()
            st.markdown(f"""
            <div class="clickable-card card-yellow">
                <h3>🟡 AI PK Zone</h3>
                <div class="value">{len(ai_pk_zone):,}</div>
                <div class="subtitle">AI Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"🔴 AI QC Center

{len(ai_qc_center):,} Orders", key="btn_ai_qc", use_container_width=True):
                st.session_state.current_view = 'ai_qc_center'
                st.rerun()
            st.markdown(f"""
            <div class="clickable-card card-red">
                <h3>🔴 AI QC Center</h3>
                <div class="value">{len(ai_qc_center):,}</div>
                <div class="subtitle">AI Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Instructions
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
            <p style="color: #666; font-size: 1.1rem; margin: 0;">
                👆 Click on any card above to view detailed orders
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.current_view == 'pk_zone':
        if st.button("← Back to Dashboard", key="back_pk"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_normal, "🟢 PK Zone - Normal Approved Orders", 
                          f"Showing {len(pk_zone_normal):,} normal orders from PK Zone", "green")
    
    elif st.session_state.current_view == 'qc_center':
        if st.button("← Back to Dashboard", key="back_qc"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_normal, "🔵 QC Center - Normal Approved Orders", 
                          f"Showing {len(qc_center_normal):,} normal orders from QC Center", "blue")
    
    elif st.session_state.current_view == 'ai_pk_zone':
        if st.button("← Back to Dashboard", key="back_ai_pk"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(ai_pk_zone, "🟡 AI Orders - PK Zone", 
                          f"Showing {len(ai_pk_zone):,} AI orders from PK Zone", "yellow")
    
    elif st.session_state.current_view == 'ai_qc_center':
        if st.button("← Back to Dashboard", key="back_ai_qc"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(ai_qc_center, "🔴 AI Orders - QC Center", 
                          f"Showing {len(ai_qc_center):,} AI orders from QC Center", "red")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem 0;">
        G-Ops Backlog Tool | Data Source: Google Sheets | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
