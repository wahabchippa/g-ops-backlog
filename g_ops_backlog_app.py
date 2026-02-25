import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="G-Ops Backlog Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# COMPLETE CSS - WITH ARROW FIX
# ============================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* ===== FIX BROKEN ARROW ICON ===== */
    [data-testid="collapsedControl"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        border: 1px solid #475569 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        top: 10px !important;
        left: 10px !important;
    }
    
    [data-testid="collapsedControl"] span {
        font-size: 0 !important;
        visibility: hidden !important;
    }
    
    [data-testid="collapsedControl"]::after {
        content: "☰";
        font-size: 22px;
        color: #3b82f6;
        visibility: visible !important;
        font-weight: bold;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
        transform: scale(1.05);
    }
    
    [data-testid="collapsedControl"]:hover::after {
        color: #60a5fa;
    }
    
    /* ===== DARK BACKGROUND ===== */
    .stApp {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
    }
    
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1600px;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0f172a 50%, #020617 100%) !important;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-bottom: 0.3rem;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-color: #3b82f6;
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 1rem;
    }
    
    .sidebar-header h2 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sidebar-header p {
        color: #64748b;
        font-size: 0.85rem;
        margin: 0.5rem 0 0 0;
    }
    
    .sidebar-stats {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar-stats-title {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-stats-value {
        color: #3b82f6;
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    .sidebar-section {
        color: #64748b;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 1rem 0 0.5rem 0;
        border-top: 1px solid #1e293b;
        margin-top: 1rem;
    }
    
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #1e293b, transparent);
        margin: 1rem 0;
    }
    
    /* ===== MAIN HEADER ===== */
    .main-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
    }
    
    .main-header-icon {
        font-size: 2.5rem;
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    
    .main-header p {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card-white {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid #e5e7eb;
    }
    
    .metric-card-white:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }
    
    .metric-card-white .label {
        color: #374151;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card-white .value {
        color: #111827;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .green-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .green-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.5);
    }
    
    .green-card .label {
        color: rgba(255,255,255,0.9);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    
    .green-card .value {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .handover-card {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .handover-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.5);
    }
    
    .handover-card .label {
        color: rgba(255,255,255,0.9);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    
    .handover-card .value {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .aging-section-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }
    
    /* ===== AGING GRID - FIXED ===== */
    .aging-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 1rem;
    }
    
    .aging-item {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 10px 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .aging-item:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-color: #3b82f6;
        transform: scale(1.05);
    }
    
    .aging-item .bucket-name {
        color: #94a3b8;
        font-size: 0.65rem;
        font-weight: 600;
        margin-bottom: 2px;
        white-space: nowrap;
    }
    
    .aging-item .bucket-count {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 800;
    }
    
    /* ===== VENDOR CARDS ===== */
    .vendor-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .vendor-card:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border-color: #3b82f6;
        transform: translateX(5px);
    }
    
    .vendor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .vendor-name-text {
        color: #e2e8f0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .vendor-count {
        background: #3b82f6;
        color: #ffffff;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    /* ===== SEARCH BOX ===== */
    .stTextInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    
    /* ===== DATAFRAME STYLING ===== */
    .stDataFrame {
        background: #1e293b;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    
    /* ===== DIVIDER ===== */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #374151, transparent);
        margin: 1.5rem 0;
    }
    
    /* ===== BACK BUTTON ===== */
    .back-btn {
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        color: #e2e8f0;
        padding: 0.5rem 1.5rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .back-btn:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }
    
    /* ===== DETAIL HEADER ===== */
    .detail-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .detail-header h2 {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .detail-header p {
        color: #94a3b8;
        font-size: 0.9rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=600)
def load_data():
    # Load main data
    main_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Extract%201"
    df = pd.read_csv(main_url)
    
    # Load AI fleek_ids
    ai_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=AI"
    ai_df = pd.read_csv(ai_url)
    ai_fleek_ids = set(ai_df['fleek_id'].dropna().astype(str).tolist())
    
    # Create derived columns
    def get_qc_zone(row):
        is_zone = str(row.get('is_zone_vendor', '')).upper() == 'TRUE'
        country = str(row.get('vendor_country', '')).upper()
        if country == 'PK':
            return 'PK Zone' if is_zone else 'PK QC Center'
        elif country == 'IN':
            return 'IN Zone' if is_zone else 'IN QC Center'
        return 'Other'
    
    df['QC or zone'] = df.apply(get_qc_zone, axis=1)
    df['Order Type'] = df['fleek_id'].astype(str).apply(lambda x: 'AI Order' if x in ai_fleek_ids else 'Normal Order')
    
    # Calculate aging
    if 'qc_approved_at' in df.columns:
        df['qc_approved_at'] = pd.to_datetime(df['qc_approved_at'], errors='coerce')
        df['aging_days'] = (datetime.now() - df['qc_approved_at']).dt.days
        df['aging_days'] = df['aging_days'].fillna(0).astype(int)
    else:
        df['aging_days'] = 0
    
    # Create aging buckets
    def get_aging_bucket(days):
        if days == 0: return '0 days'
        elif days == 1: return '1 day'
        elif days == 2: return '2 days'
        elif days == 3: return '3 days'
        elif days == 4: return '4 days'
        elif days == 5: return '5 days'
        elif days <= 7: return '6-7 days'
        elif days <= 10: return '8-10 days'
        elif days <= 15: return '11-15 days'
        elif days <= 20: return '16-20 days'
        elif days <= 25: return '21-25 days'
        elif days <= 30: return '26-30 days'
        else: return '30+ days'
    
    df['aging_bucket'] = df['aging_days'].apply(get_aging_bucket)
    
    return df

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================
# DATA SEGMENTS
# ============================================
approved_df = df[df['latest_status'] == 'QC_APPROVED']
handover_df = df[df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER']

pk_zone = approved_df[approved_df['QC or zone'] == 'PK Zone']
qc_center = approved_df[approved_df['QC or zone'] == 'PK QC Center']
pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']

# Counts
total_approved = len(approved_df)
pk_zone_count = len(pk_zone)
qc_center_count = len(qc_center)
handover_count = len(handover_df)

# ============================================
# SESSION STATE
# ============================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'aging_zone' not in st.session_state:
    st.session_state.aging_zone = None
if 'aging_bucket' not in st.session_state:
    st.session_state.aging_bucket = None
if 'vendor_name' not in st.session_state:
    st.session_state.vendor_name = None
if 'vendor_zone' not in st.session_state:
    st.session_state.vendor_zone = None
if 'handover_bucket' not in st.session_state:
    st.session_state.handover_bucket = None
if 'vendor_comments' not in st.session_state:
    st.session_state.vendor_comments = {}
if 'search_result_vendor' not in st.session_state:
    st.session_state.search_result_vendor = None

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    # Header
    st.markdown("""
        <div class="sidebar-header">
            <h2>⚡ G-Ops Backlog</h2>
            <p>Operations Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown(f"""
        <div class="sidebar-stats">
            <div class="sidebar-stats-title">Total Approved</div>
            <div class="sidebar-stats-value">{total_approved:,}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown('<div class="sidebar-section">📍 Navigation</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Dashboard", key="nav_home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button(f"📦 Handover ({handover_count:,})", key="nav_handover", use_container_width=True):
        st.session_state.page = 'handover'
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">🇵🇰 PK Zone Orders</div>', unsafe_allow_html=True)
    
    if st.button(f"📋 Normal Orders ({len(pk_normal):,})", key="nav_pk_normal", use_container_width=True):
        st.session_state.page = 'pk_normal'
        st.rerun()
    
    if st.button(f"🤖 AI Orders ({len(pk_ai):,})", key="nav_pk_ai", use_container_width=True):
        st.session_state.page = 'pk_ai'
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">🏢 QC Center Orders</div>', unsafe_allow_html=True)
    
    if st.button(f"📋 Normal Orders ({len(qc_normal):,})", key="nav_qc_normal", use_container_width=True):
        st.session_state.page = 'qc_normal'
        st.rerun()
    
    if st.button(f"🤖 AI Orders ({len(qc_ai):,})", key="nav_qc_ai", use_container_width=True):
        st.session_state.page = 'qc_ai'
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Refresh button
    if st.button("🔄 Refresh Data", key="refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    # Last updated
    st.markdown(f"""
        <div style="text-align: center; color: #64748b; font-size: 0.75rem; margin-top: 1rem;">
            Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}
        </div>
    """, unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================
def render_aging_pivot(data, title, zone_key):
    """Render aging analysis with clickable buttons - 2 rows of 4"""
    bucket_order = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                    '6-7 days', '8-10 days', '11-15 days', '16-20 days', 
                    '21-25 days', '26-30 days', '30+ days']
    
    aging_counts = data.groupby('aging_bucket').size().reindex(bucket_order, fill_value=0)
    
    st.markdown(f'<div class="aging-section-title">{title}</div>', unsafe_allow_html=True)
    
    # Row 1: First 7 buckets (0-6-7 days)
    cols1 = st.columns(7)
    for i, bucket in enumerate(bucket_order[:7]):
        count = aging_counts.get(bucket, 0)
        with cols1[i]:
            short_label = bucket.replace(' days', 'd').replace(' day', 'd')
            if st.button(f"{short_label}\n{count}", key=f"aging_{zone_key}_{bucket}", use_container_width=True):
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = zone_key
                st.session_state.aging_bucket = bucket
                st.rerun()
    
    # Row 2: Remaining 6 buckets
    cols2 = st.columns(6)
    for i, bucket in enumerate(bucket_order[7:]):
        count = aging_counts.get(bucket, 0)
        with cols2[i]:
            short_label = bucket.replace(' days', 'd')
            if st.button(f"{short_label}\n{count}", key=f"aging_{zone_key}_{bucket}", use_container_width=True):
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = zone_key
                st.session_state.aging_bucket = bucket
                st.rerun()

def render_vendor_table(data, zone_key, limit=10):
    """Render vendor table with counts and comments"""
    vendor_counts = data.groupby('vendor').size().reset_index(name='count')
    vendor_counts = vendor_counts.sort_values('count', ascending=False).head(limit)
    
    comment_options = ['--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']
    
    for _, row in vendor_counts.iterrows():
        vendor = str(row['vendor'])
        count = row['count']
        
        col1, col2, col3 = st.columns([3, 1, 2])
        
        with col1:
            if st.button(f"🏪 {vendor[:20]}", key=f"vendor_{zone_key}_{vendor}", use_container_width=True):
                st.session_state.page = 'vendor_detail'
                st.session_state.vendor_name = vendor
                st.session_state.vendor_zone = zone_key
                st.rerun()
        
        with col2:
            st.markdown(f'<div style="background: #3b82f6; color: white; padding: 0.5rem; border-radius: 8px; text-align: center; font-weight: 700;">{count}</div>', unsafe_allow_html=True)
        
        with col3:
            comment_key = f"{zone_key}_{vendor}"
            current_comment = st.session_state.vendor_comments.get(comment_key, '--')
            new_comment = st.selectbox(
                "Action",
                comment_options,
                index=comment_options.index(current_comment) if current_comment in comment_options else 0,
                key=f"comment_{zone_key}_{vendor}",
                label_visibility="collapsed"
            )
            if new_comment != current_comment:
                st.session_state.vendor_comments[comment_key] = new_comment

def render_orders_table(data):
    """Render orders dataframe"""
    display_cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                    'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
                    'logistics_partner_name', 'aging_days', 'aging_bucket']
    
    available_cols = [c for c in display_cols if c in data.columns]
    
    if len(data) > 0:
        st.dataframe(data[available_cols], use_container_width=True, height=400)
        
        # Download button
        csv = data[available_cols].to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"orders_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No orders found")

# ============================================
# MAIN CONTENT - HOME PAGE
# ============================================
if st.session_state.page == 'home':
    # Header
    st.markdown("""
        <div class="main-header">
            <span class="main-header-icon">⚡</span>
            <div>
                <h1>G-Ops Backlog Dashboard</h1>
                <p>📊 Real-time Operations Monitoring | Last updated: """ + datetime.now().strftime('%d %b %Y, %I:%M %p') + """</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Search box
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        search_query = st.text_input("", placeholder="Enter Order Number or Vendor Name...", label_visibility="collapsed")
    with col2:
        search_clicked = st.button("🔍 Search", use_container_width=True)
    
    if search_clicked and search_query:
        search_results = approved_df[
            (approved_df['order_number'].astype(str).str.contains(search_query, case=False, na=False)) |
            (approved_df['vendor'].astype(str).str.contains(search_query, case=False, na=False))
        ]
        
        if len(search_results) > 0:
            st.success(f"Found {len(search_results)} orders")
            render_orders_table(search_results)
        else:
            st.warning("No orders found matching your search")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card-white">
                <div class="label">TOTAL APPROVED</div>
                <div class="value">{total_approved:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card-white">
                <div class="label">PK ZONE</div>
                <div class="value">{pk_zone_count:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card-white">
                <div class="label">QC CENTER</div>
                <div class="value">{qc_center_count:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="handover-card">
                <div class="label">HANDOVER</div>
                <div class="value">{handover_count:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Three Column Layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="section-title">📦 Handover</div>', unsafe_allow_html=True)
        render_aging_pivot(handover_df, "Aging Analysis", "handover")
    
    with col2:
        st.markdown('<div class="section-title">🇵🇰 PK Zone</div>', unsafe_allow_html=True)
        render_aging_pivot(pk_zone, "Aging Analysis", "pk_zone")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("**Top Vendors**")
        render_vendor_table(pk_zone, "pk_zone", limit=10)
    
    with col3:
        st.markdown('<div class="section-title">🏢 QC Center</div>', unsafe_allow_html=True)
        render_aging_pivot(qc_center, "Aging Analysis", "qc_center")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("**Top Vendors**")
        render_vendor_table(qc_center, "qc_center", limit=10)

# ============================================
# HANDOVER PAGE
# ============================================
elif st.session_state.page == 'handover':
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>📦 Handover Orders</h2>
            <p>Total: {handover_count:,} orders handed over to logistics partner</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(handover_df, "Aging Analysis", "handover_page")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(handover_df)

# ============================================
# PK NORMAL PAGE
# ============================================
elif st.session_state.page == 'pk_normal':
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>🇵🇰 PK Zone - Normal Orders</h2>
            <p>Total: {len(pk_normal):,} normal orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(pk_normal, "Aging Analysis", "pk_normal_page")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Vendors**")
    render_vendor_table(pk_normal, "pk_normal_v", limit=50)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(pk_normal)

# ============================================
# PK AI PAGE
# ============================================
elif st.session_state.page == 'pk_ai':
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>🇵🇰 PK Zone - AI Orders</h2>
            <p>Total: {len(pk_ai):,} AI orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(pk_ai, "Aging Analysis", "pk_ai_page")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Vendors**")
    render_vendor_table(pk_ai, "pk_ai_v", limit=50)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(pk_ai)

# ============================================
# QC NORMAL PAGE
# ============================================
elif st.session_state.page == 'qc_normal':
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>🏢 QC Center - Normal Orders</h2>
            <p>Total: {len(qc_normal):,} normal orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(qc_normal, "Aging Analysis", "qc_normal_page")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Vendors**")
    render_vendor_table(qc_normal, "qc_normal_v", limit=50)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(qc_normal)

# ============================================
# QC AI PAGE
# ============================================
elif st.session_state.page == 'qc_ai':
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>🏢 QC Center - AI Orders</h2>
            <p>Total: {len(qc_ai):,} AI orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(qc_ai, "Aging Analysis", "qc_ai_page")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Vendors**")
    render_vendor_table(qc_ai, "qc_ai_v", limit=50)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(qc_ai)

# ============================================
# AGING DETAIL PAGE
# ============================================
elif st.session_state.page == 'aging_detail':
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    zone = st.session_state.aging_zone
    bucket = st.session_state.aging_bucket
    
    # Get correct dataset based on zone
    zone_map = {
        'handover': (handover_df, "📦 Handover"),
        'handover_page': (handover_df, "📦 Handover"),
        'pk_zone': (pk_zone, "🇵🇰 PK Zone"),
        'qc_center': (qc_center, "🏢 QC Center"),
        'pk_normal': (pk_normal, "🇵🇰 PK Zone Normal"),
        'pk_normal_page': (pk_normal, "🇵🇰 PK Zone Normal"),
        'pk_ai': (pk_ai, "🇵🇰 PK Zone AI"),
        'pk_ai_page': (pk_ai, "🇵🇰 PK Zone AI"),
        'qc_normal': (qc_normal, "🏢 QC Center Normal"),
        'qc_normal_page': (qc_normal, "🏢 QC Center Normal"),
        'qc_ai': (qc_ai, "🏢 QC Center AI"),
        'qc_ai_page': (qc_ai, "🏢 QC Center AI"),
    }
    
    if zone in zone_map:
        base_data, zone_label = zone_map[zone]
        data = base_data[base_data['aging_bucket'] == bucket]
        title = f"{zone_label} - {bucket}"
    else:
        data = pd.DataFrame()
        title = "Orders"
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>{title}</h2>
            <p>Total: {len(data):,} orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_orders_table(data)

# ============================================
# VENDOR DETAIL PAGE
# ============================================
elif st.session_state.page == 'vendor_detail':
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    vendor = st.session_state.vendor_name
    zone = st.session_state.vendor_zone
    
    # Get correct dataset
    zone_map = {
        'pk_zone': (pk_zone, "PK Zone"),
        'qc_center': (qc_center, "QC Center"),
        'pk_normal': (pk_normal, "PK Zone Normal"),
        'pk_normal_v': (pk_normal, "PK Zone Normal"),
        'pk_ai': (pk_ai, "PK Zone AI"),
        'pk_ai_v': (pk_ai, "PK Zone AI"),
        'qc_normal': (qc_normal, "QC Center Normal"),
        'qc_normal_v': (qc_normal, "QC Center Normal"),
        'qc_ai': (qc_ai, "QC Center AI"),
        'qc_ai_v': (qc_ai, "QC Center AI"),
    }
    
    if zone in zone_map:
        base_data, zone_label = zone_map[zone]
        data = base_data[base_data['vendor'].astype(str) == vendor]
    else:
        data = pd.DataFrame()
        zone_label = ""
    
    st.markdown(f"""
        <div class="detail-header">
            <h2>🏪 {vendor}</h2>
            <p>{zone_label} | Total: {len(data):,} orders</p>
        </div>
    """, unsafe_allow_html=True)
    
    render_aging_pivot(data, "Aging Analysis", f"vendor_{zone}_detail")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    render_orders_table(data)
