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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        margin: 0;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.8rem;
        font-weight: 400;
    }
    
    /* Section container */
    .section-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Section header */
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f5;
    }
    .section-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    .section-icon.green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .section-icon.blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0;
    }
    .section-subtitle {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
    }
    
    /* Order cards */
    .order-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    .order-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        border-color: transparent;
    }
    .order-card.normal {
        border-left: 4px solid #28a745;
    }
    .order-card.normal:hover {
        background: linear-gradient(135deg, #d4edda 0%, #ffffff 100%);
    }
    .order-card.ai {
        border-left: 4px solid #ffc107;
    }
    .order-card.ai:hover {
        background: linear-gradient(135deg, #fff3cd 0%, #ffffff 100%);
    }
    
    .order-card .card-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .order-card.normal .card-label { color: #28a745; }
    .order-card.ai .card-label { color: #d39e00; }
    
    .order-card .card-value {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0.3rem 0;
    }
    .order-card.normal .card-value { color: #1e7e34; }
    .order-card.ai .card-value { color: #d39e00; }
    
    .order-card .card-desc {
        font-size: 0.85rem;
        color: #666;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.2);
        border-color: rgba(255,255,255,0.4);
    }
    
    /* Main content buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Page header for detail pages */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .page-header h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .page-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
    }
    .stat-item {
        text-align: center;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
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

def display_orders_page(df, title, subtitle):
    """Display orders in a professional table format"""
    
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
        search = st.text_input("Search by Order #, Customer, Fleek ID", "", key=f"search_{title}")
    with col2:
        if 'customer_country' in df.columns:
            countries = ['All Countries'] + sorted(df['customer_country'].dropna().unique().tolist())
            country = st.selectbox("Country", countries, key=f"country_{title}")
        else:
            country = "All Countries"
    with col3:
        st.write("")
        st.write("")
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, f"orders_export.csv", "text/csv", key=f"csv_{title}")
    
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
    
    st.write(f"**Showing {len(filtered_df):,} orders**")
    
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
    
    # PK Zone Orders
    pk_zone_normal = pd.DataFrame()
    pk_zone_ai = pd.DataFrame()
    if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns:
        pk_zone_normal = approved_df[
            (approved_df['QC or zone'] == 'PK Zone') & 
            (approved_df['Order Type'] == 'Normal Order')
        ]
        pk_zone_ai = approved_df[
            (approved_df['QC or zone'] == 'PK Zone') & 
            (approved_df['Order Type'] == 'AI Order')
        ]
    
    # QC Center Orders
    qc_center_normal = pd.DataFrame()
    qc_center_ai = pd.DataFrame()
    if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns:
        qc_center_normal = approved_df[
            (approved_df['QC or zone'] == 'PK QC Center') & 
            (approved_df['Order Type'] == 'Normal Order')
        ]
        qc_center_ai = approved_df[
            (approved_df['QC or zone'] == 'PK QC Center') & 
            (approved_df['Order Type'] == 'AI Order')
        ]
    
    # Counts
    pk_normal_count = len(pk_zone_normal)
    pk_ai_count = len(pk_zone_ai)
    qc_normal_count = len(qc_center_normal)
    qc_ai_count = len(qc_center_ai)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### G-Ops Backlog")
        st.caption("Operations Management Tool")
        
        st.markdown("---")
        
        if st.button("Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### Quick Stats")
        
        st.markdown(f"""
        **PK Zone**  
        Normal: {pk_normal_count:,} | AI: {pk_ai_count:,}
        
        **QC Center**  
        Normal: {qc_normal_count:,} | AI: {qc_ai_count:,}
        """)
        
        st.markdown("---")
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.caption(f"Updated: {now}")
    
    # Main content
    if st.session_state.current_view == 'dashboard':
        # Dashboard Header
        st.markdown("""
        <div class="main-header">
            <h1>G-Ops Backlog Dashboard</h1>
            <p>Real-time Operations Tracking & Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== PK ZONE SECTION ==========
        st.markdown("""
        <div class="section-container">
            <div class="section-header">
                <div class="section-icon green">🏭</div>
                <div>
                    <h3 class="section-title">PK Zone Orders</h3>
                    <p class="section-subtitle">Approved orders from Pakistan Zone</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="order-card normal">
                <div class="card-label">Normal Orders</div>
                <div class="card-value">{pk_normal_count:,}</div>
                <div class="card-desc">Click to view details</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Normal Orders", key="pk_normal_btn", use_container_width=True):
                st.session_state.current_view = 'pk_zone_normal'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card ai">
                <div class="card-label">AI Orders</div>
                <div class="card-value">{pk_ai_count:,}</div>
                <div class="card-desc">Click to view details</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View AI Orders", key="pk_ai_btn", use_container_width=True):
                st.session_state.current_view = 'pk_zone_ai'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== QC CENTER SECTION ==========
        st.markdown("""
        <div class="section-container">
            <div class="section-header">
                <div class="section-icon blue">🏢</div>
                <div>
                    <h3 class="section-title">QC Center Orders</h3>
                    <p class="section-subtitle">Approved orders from QC Center</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="order-card normal">
                <div class="card-label">Normal Orders</div>
                <div class="card-value">{qc_normal_count:,}</div>
                <div class="card-desc">Click to view details</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Normal Orders", key="qc_normal_btn", use_container_width=True):
                st.session_state.current_view = 'qc_center_normal'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card ai">
                <div class="card-label">AI Orders</div>
                <div class="card-value">{qc_ai_count:,}</div>
                <div class="card-desc">Click to view details</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View AI Orders", key="qc_ai_btn", use_container_width=True):
                st.session_state.current_view = 'qc_center_ai'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Detail Pages
    elif st.session_state.current_view == 'pk_zone_normal':
        if st.button("Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_normal, "PK Zone - Normal Orders", 
                          f"{pk_normal_count:,} approved normal orders from PK Zone")
    
    elif st.session_state.current_view == 'pk_zone_ai':
        if st.button("Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_ai, "PK Zone - AI Orders", 
                          f"{pk_ai_count:,} approved AI orders from PK Zone")
    
    elif st.session_state.current_view == 'qc_center_normal':
        if st.button("Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_normal, "QC Center - Normal Orders", 
                          f"{qc_normal_count:,} approved normal orders from QC Center")
    
    elif st.session_state.current_view == 'qc_center_ai':
        if st.button("Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_ai, "QC Center - AI Orders", 
                          f"{qc_ai_count:,} approved AI orders from QC Center")
    
    # Footer
    st.markdown("---")
    now_footer = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.caption(f"G-Ops Backlog Tool | Data Source: Google Sheets | Updated: {now_footer}")

if __name__ == "__main__":
    main()
