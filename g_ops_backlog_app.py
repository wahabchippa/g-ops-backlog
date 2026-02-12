import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="📦", layout="wide")

# Session state
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

# Initialize vendor comments storage
if 'vendor_comments' not in st.session_state:
    st.session_state.vendor_comments = {}

# Dynamic Theme based on page
if st.session_state.page == 'home':
    # DARK WOVEN/TEXTURED THEME for Home
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        background-color: #1a1a1a;
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Beautiful Title - Light for Dark BG */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 50%, #d0d0d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #a0a0a0;
        font-size: 0.95rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Light Section Headers - Visible on Dark BG */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e0e0e0;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #444444;
    }
    
    /* Metric Cards - Dark with light text */
    .metric-card {
        background: rgba(50,50,50,0.9);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.2);
        border: 1px solid #444444;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }
    
    .metric-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
    }
    
    /* Light Buttons with Hover Effect */
    .stButton > button {
        background: rgba(60,60,60,0.9) !important;
        color: #e0e0e0 !important;
        border: 2px solid #555555 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4a4a4a 0%, #5a5a5a 100%) !important;
        color: white !important;
        border-color: #666666 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    /* Info Cards */
    .info-card {
        background: rgba(50,50,50,0.9);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border-left: 5px solid #666666;
    }
    
    .info-title {
        font-weight: 600;
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .info-value {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }
    
    /* Dropdown Styling */
    .stSelectbox > div > div {
        background: rgba(60,60,60,0.9) !important;
        border: 2px solid #555555 !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }
    
    .stSelectbox label {
        color: #a0a0a0 !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #444444;
        margin: 35px 0;
    }
    
    /* Text Colors for Dark Background */
    .stMarkdown, p, span, label { color: #e0e0e0 !important; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    
    /* Caption styling */
    .stCaption, small { color: #909090 !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #2a2a2a; }
    ::-webkit-scrollbar-thumb { background: #555555; border-radius: 4px; }
    
    /* Table header styling */
    .vendor-header {
        color: #ffffff;
        font-weight: 700;
        padding: 10px 0;
        border-bottom: 2px solid #444444;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # DARK THEME for Detail Pages (same as before)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 50%, #0c0a1d 100%);
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Page Title */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 5px;
    }
    
    .page-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Back Button */
    .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        color: #60a5fa !important;
        border: 2px solid rgba(96,165,250,0.3) !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #60a5fa !important;
        color: #0f172a !important;
        border-color: #60a5fa !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(96,165,250,0.3);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #f1f5f9 !important;
        border: 2px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 20px rgba(96,165,250,0.2) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 20px rgba(16,185,129,0.3);
    }
    
    /* DataFrame */
    [data-testid="stDataFrame"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Text Colors */
    p, span, label, .stMarkdown { color: #e2e8f0 !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%); border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# Data Loading - OPTIMIZED
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

# Only load columns we need - HUGE speed boost
REQUIRED_COLS = [
    'latest_status', 'QC or zone', 'Order Type', 'order_number', 'fleek_id',
    'customer_name', 'customer_country', 'vendor', 'item_name', 
    'total_order_line_amount', 'product_brand', 'logistics_partner_name',
    'qc_approved_at', 'logistics_partner_handedover_at'
]

@st.cache_data(ttl=600, show_spinner=False)  # 10 min cache
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
    df = pd.read_csv(url, usecols=lambda c: c in REQUIRED_COLS, low_memory=False)
    return df

@st.cache_data(ttl=600, show_spinner=False)
def process_data(df):
    """Process data once and cache it"""
    now = datetime.now()
    
    # Filter data
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))].copy()
    
    # Vectorized date parsing - MUCH faster than .apply()
    approved['qc_date'] = pd.to_datetime(approved['qc_approved_at'], format='%B %d, %Y, %H:%M', errors='coerce')
    approved['aging_days'] = (now - approved['qc_date']).dt.days
    
    handover['handover_date'] = pd.to_datetime(handover['logistics_partner_handedover_at'], format='%B %d, %Y, %H:%M', errors='coerce')
    handover['aging_days'] = (now - handover['handover_date']).dt.days
    
    # Vectorized bucket assignment - faster than .apply()
    def assign_buckets(days_series):
        conditions = [
            days_series == 0,
            days_series == 1,
            days_series == 2,
            days_series == 3,
            days_series == 4,
            days_series == 5,
            (days_series >= 6) & (days_series <= 7),
            (days_series >= 8) & (days_series <= 10),
            (days_series >= 11) & (days_series <= 15),
            (days_series >= 16) & (days_series <= 20),
            (days_series >= 21) & (days_series <= 25),
            (days_series >= 26) & (days_series <= 30),
            days_series > 30
        ]
        choices = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days',
                   '6-7 days', '8-10 days', '11-15 days', '16-20 days',
                   '21-25 days', '26-30 days', '30+ days']
        import numpy as np
        return np.select(conditions, choices, default=None)
    
    approved['aging_bucket'] = assign_buckets(approved['aging_days'])
    handover['aging_bucket'] = assign_buckets(handover['aging_days'])
    
    # Pre-filter all subsets
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
    pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
    qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
    qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']
    
    return {
        'approved': approved,
        'handover': handover,
        'pk_zone': pk_zone,
        'qc_center': qc_center,
        'pk_normal': pk_normal,
        'pk_ai': pk_ai,
        'qc_normal': qc_normal,
        'qc_ai': qc_ai
    }

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                '6-7 days', '8-10 days', '11-15 days', '16-20 days', 
                '21-25 days', '26-30 days', '30+ days']

# Dropdown options for vendors - with Remove option
VENDOR_ACTION_OPTIONS = ['-- Select --', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']

DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
                'logistics_partner_name', 'aging_days', 'aging_bucket']

try:
    # Show loading spinner only on first load
    with st.spinner('Loading data...'):
        df = load_data()
        data = process_data(df)
    
    # Extract processed data
    approved = data['approved']
    handover = data['handover']
    pk_zone = data['pk_zone']
    qc_center = data['qc_center']
    pk_normal = data['pk_normal']
    pk_ai = data['pk_ai']
    qc_normal = data['qc_normal']
    qc_ai = data['qc_ai']

    # ==================== HOME PAGE ====================
    if st.session_state.page == 'home':
        
        # Beautiful Title with Icon
        st.markdown("""
            <div style="margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 3.5rem;">📦</span>
                    <span class="main-title">G-Ops Backlog Dashboard</span>
                </div>
                <p class="subtitle">✨ Real-time operations tracking • Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            (col1, "Total Approved", len(approved)),
            (col2, "PK Zone", len(pk_zone)),
            (col3, "QC Center", len(qc_center)),
            (col4, "Handover", len(handover))
        ]
        for col, label, value in metrics:
            with col:
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value:,}</div>
                    </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Handover Section
        st.markdown('<div class="section-header">🚚 Handover to Logistics</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f'''
                <div class="info-card">
                    <div class="info-title">Orders handed over to logistics partner</div>
                    <div class="info-value">{len(handover):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.write("")
            if st.button("View Orders", key="v_handover"):
                st.session_state.page = 'handover'
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # PK Zone Section
        st.markdown('<div class="section-header">📍 PK Zone Orders</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Normal Orders</div><div class="metric-value">{len(pk_normal):,}</div></div>', unsafe_allow_html=True)
        with col2:
            st.write(""); st.write("")
            if st.button("View", key="v_pk_n"):
                st.session_state.page = 'pk_normal'
                st.rerun()
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">AI Orders</div><div class="metric-value">{len(pk_ai):,}</div></div>', unsafe_allow_html=True)
        with col4:
            st.write(""); st.write("")
            if st.button("View", key="v_pk_a"):
                st.session_state.page = 'pk_ai'
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # QC Center Section
        st.markdown('<div class="section-header">🏢 QC Center Orders</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Normal Orders</div><div class="metric-value">{len(qc_normal):,}</div></div>', unsafe_allow_html=True)
        with col2:
            st.write(""); st.write("")
            if st.button("View", key="v_qc_n"):
                st.session_state.page = 'qc_normal'
                st.rerun()
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">AI Orders</div><div class="metric-value">{len(qc_ai):,}</div></div>', unsafe_allow_html=True)
        with col4:
            st.write(""); st.write("")
            if st.button("View", key="v_qc_a"):
                st.session_state.page = 'qc_ai'
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ AGING PIVOT TABLES - CLICKABLE ============
        st.markdown('<div class="section-header">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
        st.caption("🖱️ Click on count to view orders for that aging bucket")
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        # PK Zone Aging - Clickable with visible labels
        with col1:
            st.markdown("##### 📍 PK Zone Normal")
            h1, h2 = st.columns([3, 1])
            with h1:
                st.markdown("**Aging Bucket**")
            with h2:
                st.markdown("**Count**")
            
            for bucket in BUCKET_ORDER:
                count = pk_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<div style='padding: 6px 0; color: #e0e0e0; font-size: 0.9rem; font-weight: 500;'>{bucket}</div>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"pk_aging_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK Zone'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown(f"<div style='padding: 8px; text-align: center; color: #707070;'>0</div>", unsafe_allow_html=True)
            st.markdown(f"**Total: {len(pk_normal):,}**")
        
        # QC Center Aging - Clickable with visible labels
        with col2:
            st.markdown("##### 🏢 QC Center Normal")
            h1, h2 = st.columns([3, 1])
            with h1:
                st.markdown("**Aging Bucket**")
            with h2:
                st.markdown("**Count**")
            
            for bucket in BUCKET_ORDER:
                count = qc_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<div style='padding: 6px 0; color: #e0e0e0; font-size: 0.9rem; font-weight: 500;'>{bucket}</div>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"qc_aging_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK QC Center'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown(f"<div style='padding: 8px; text-align: center; color: #707070;'>0</div>", unsafe_allow_html=True)
            st.markdown(f"**Total: {len(qc_normal):,}**")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ PK ZONE VENDOR TABLE ONLY - WITH PERSISTENT COMMENTS ============
        st.markdown('<div class="section-header">🏪 PK Zone Vendors - Normal Orders</div>', unsafe_allow_html=True)
        st.caption("🖱️ Click on order count to view vendor's orders | Comment is saved automatically")
        
        pk_vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        pk_vendor_counts.columns = ['Vendor', 'Orders']
        
        # Header row with Comment
        h1, h2, h3 = st.columns([4, 1, 2])
        with h1:
            st.markdown("**Vendor Name**")
        with h2:
            st.markdown("**Orders**")
        with h3:
            st.markdown("**Comment**")
        
        for i, (_, row) in enumerate(pk_vendor_counts.iterrows()):
            vendor_key = f"pk_{row['Vendor']}"
            c1, c2, c3 = st.columns([4, 1, 2])
            with c1:
                vendor_display = row['Vendor'][:40] + "..." if len(str(row['Vendor'])) > 40 else row['Vendor']
                st.markdown(f"<div style='padding: 8px 0; color: #e0e0e0; font-size: 0.9rem; font-weight: 500;'>{vendor_display}</div>", unsafe_allow_html=True)
            with c2:
                if st.button(f"{row['Orders']}", key=f"pk_vendor_{i}", use_container_width=True):
                    st.session_state.page = 'vendor_detail'
                    st.session_state.vendor_name = row['Vendor']
                    st.session_state.vendor_zone = 'PK Zone'
                    st.rerun()
            with c3:
                # Get current saved value or default
                current_value = st.session_state.vendor_comments.get(vendor_key, '-- Select --')
                
                # Find index of current value
                try:
                    default_index = VENDOR_ACTION_OPTIONS.index(current_value)
                except ValueError:
                    default_index = 0
                
                # Dropdown with saved value
                selected = st.selectbox(
                    "", 
                    VENDOR_ACTION_OPTIONS, 
                    index=default_index,
                    key=f"pk_action_{i}", 
                    label_visibility="collapsed"
                )
                
                # Save selection (handle Remove)
                if selected == '❌ Remove':
                    if vendor_key in st.session_state.vendor_comments:
                        del st.session_state.vendor_comments[vendor_key]
                elif selected != '-- Select --':
                    st.session_state.vendor_comments[vendor_key] = selected
        
        st.markdown(f"**Total: {len(pk_vendor_counts)} vendors | {len(pk_normal):,} orders**")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ HANDOVER AGING ============
        st.markdown('<div class="section-header">🚚 Handover Aging Analysis</div>', unsafe_allow_html=True)
        st.caption("🖱️ Click on count to view handover orders for that aging bucket")
        
        handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        h1, h2 = st.columns([3, 1])
        with h1:
            st.markdown("**Aging Bucket**")
        with h2:
            st.markdown("**Count**")
        
        for bucket in BUCKET_ORDER:
            count = handover_aging.get(bucket, 0)
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"<div style='padding: 6px 0; color: #e0e0e0; font-size: 0.9rem; font-weight: 500;'>{bucket}</div>", unsafe_allow_html=True)
            with c2:
                if count > 0:
                    if st.button(f"{count}", key=f"handover_aging_{bucket}", use_container_width=True):
                        st.session_state.page = 'handover_aging_detail'
                        st.session_state.handover_bucket = bucket
                        st.rerun()
                else:
                    st.markdown(f"<div style='padding: 8px; text-align: center; color: #707070;'>0</div>", unsafe_allow_html=True)
        
        st.markdown(f"**Total Handover: {len(handover):,} orders**")

    # ==================== DETAIL PAGES (DARK) ====================
    else:
        if st.button("← Back to Dashboard", key="back"):
            st.session_state.page = 'home'
            st.rerun()
        
        st.write("")
        
        page = st.session_state.page
        
        if page == 'handover':
            title = "🚚 Handover Orders"
            data_view = handover
        elif page == 'pk_normal':
            title = "📍 PK Zone - Normal Orders"
            data_view = pk_normal
        elif page == 'pk_ai':
            title = "📍 PK Zone - AI Orders"
            data_view = pk_ai
        elif page == 'qc_normal':
            title = "🏢 QC Center - Normal Orders"
            data_view = qc_normal
        elif page == 'qc_ai':
            title = "🏢 QC Center - AI Orders"
            data_view = qc_ai
        elif page == 'aging_detail':
            zone = st.session_state.aging_zone
            bucket = st.session_state.aging_bucket
            icon = "📍" if zone == 'PK Zone' else "🏢"
            title = f"{icon} {zone} - {bucket} Aging"
            if zone == 'PK Zone':
                data_view = pk_normal[pk_normal['aging_bucket'] == bucket]
            else:
                data_view = qc_normal[qc_normal['aging_bucket'] == bucket]
        elif page == 'vendor_detail':
            vendor = st.session_state.vendor_name
            zone = st.session_state.vendor_zone
            icon = "📍" if zone == 'PK Zone' else "🏢"
            title = f"{icon} {zone} Vendor: {vendor}"
            if zone == 'PK Zone':
                data_view = pk_normal[pk_normal['vendor'] == vendor]
            else:
                data_view = qc_normal[qc_normal['vendor'] == vendor]
        elif page == 'handover_aging_detail':
            bucket = st.session_state.handover_bucket
            title = f"🚚 Handover - {bucket} Aging"
            data_view = handover[handover['aging_bucket'] == bucket]
        else:
            title = "📋 Orders"
            data_view = approved
        
        st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">📋 {len(data_view):,} orders found</div>', unsafe_allow_html=True)
        
        st.write("")
        
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order number, customer name, vendor...")
        with col2:
            countries = ['All Countries'] + sorted(data_view['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Filter by Country", countries)
        with col3:
            st.write(""); st.write("")
            st.download_button("📥 Export CSV", data_view.to_csv(index=False), "orders.csv", "text/csv", use_container_width=True)
        
        st.write("")
        
        filtered = data_view.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['vendor'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All Countries':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.markdown(f'<p style="color: #94a3b8; margin-bottom: 10px;">Showing {len(filtered):,} of {len(data_view):,} orders</p>', unsafe_allow_html=True)
        
        display_df = filtered[[c for c in DISPLAY_COLS if c in filtered.columns]]
        st.dataframe(display_df, use_container_width=True, height=600)

except Exception as e:
    st.error(f"Error loading data: {e}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
