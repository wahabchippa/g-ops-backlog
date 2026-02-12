import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="🚀", layout="wide")

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
    # DARK BACKGROUND WITH WHITE CARDS
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
    
    /* BIG Beautiful Title - Light for Dark BG */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 50%, #c0c0c0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(255,255,255,0.1);
    }
    
    .title-icon {
        font-size: 3.2rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .subtitle {
        color: #a0a0a0;
        font-size: 0.85rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Light Section Headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e0e0e0;
        margin: 20px 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #444444;
    }
    
    /* WHITE Metric Cards with DARK text */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid #e0e0e0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .metric-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #1a1a1a;
    }
    
    /* Buttons - Light style */
    .stButton > button {
        background: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
        padding: 4px 12px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        transition: all 0.3s ease !important;
        min-height: 32px !important;
    }
    
    .stButton > button:hover {
        background: #f0f0f0 !important;
        color: #000000 !important;
        border-color: #999999 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* WHITE Info Cards with DARK text */
    .info-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border-left: 4px solid #333333;
    }
    
    .info-title {
        font-weight: 600;
        color: #666666;
        font-size: 0.75rem;
        margin-bottom: 5px;
    }
    
    .info-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a1a1a;
    }
    
    /* Dropdown Styling - White */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
        color: #333333 !important;
        font-size: 0.75rem !important;
        min-height: 32px !important;
    }
    
    .stSelectbox label {
        color: #a0a0a0 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #444444;
        margin: 20px 0;
    }
    
    /* Text Colors */
    .stMarkdown, p, span, label { color: #e0e0e0 !important; font-size: 0.8rem !important; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    
    /* Caption styling */
    .stCaption, small { color: #808080 !important; font-size: 0.7rem !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #2a2a2a; }
    ::-webkit-scrollbar-thumb { background: #555555; border-radius: 3px; }
    
    /* WHITE Aging Table */
    .aging-table {
        background: #ffffff;
        border-radius: 10px;
        padding: 12px;
        margin-top: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* WHITE Vendor Table */
    .vendor-table {
        background: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Table Headers - Dark on white */
    .table-header {
        font-size: 0.7rem;
        font-weight: 700;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # DARK THEME for Detail Pages
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 50%, #0c0a1d 100%);
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 5px;
    }
    
    .page-subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        color: #60a5fa !important;
        border: 1px solid rgba(96,165,250,0.3) !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #60a5fa !important;
        color: #0f172a !important;
        border-color: #60a5fa !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-size: 0.8rem !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    p, span, label, .stMarkdown { color: #e2e8f0 !important; font-size: 0.8rem !important; }
    
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb { background: #60a5fa; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)

# Data Loading
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

REQUIRED_COLS = [
    'latest_status', 'QC or zone', 'Order Type', 'order_number', 'fleek_id',
    'customer_name', 'customer_country', 'vendor', 'item_name', 
    'total_order_line_amount', 'product_brand', 'logistics_partner_name',
    'qc_approved_at', 'logistics_partner_handedover_at'
]

@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
    df = pd.read_csv(url, usecols=lambda c: c in REQUIRED_COLS, low_memory=False)
    return df

@st.cache_data(ttl=600, show_spinner=False)
def process_data(df):
    now = datetime.now()
    
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))].copy()
    
    approved['qc_date'] = pd.to_datetime(approved['qc_approved_at'], format='%B %d, %Y, %H:%M', errors='coerce')
    approved['aging_days'] = (now - approved['qc_date']).dt.days
    
    handover['handover_date'] = pd.to_datetime(handover['logistics_partner_handedover_at'], format='%B %d, %Y, %H:%M', errors='coerce')
    handover['aging_days'] = (now - handover['handover_date']).dt.days
    
    def assign_buckets(days_series):
        import numpy as np
        conditions = [
            days_series == 0, days_series == 1, days_series == 2, days_series == 3,
            days_series == 4, days_series == 5, (days_series >= 6) & (days_series <= 7),
            (days_series >= 8) & (days_series <= 10), (days_series >= 11) & (days_series <= 15),
            (days_series >= 16) & (days_series <= 20), (days_series >= 21) & (days_series <= 25),
            (days_series >= 26) & (days_series <= 30), days_series > 30
        ]
        choices = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days',
                   '6-7 days', '8-10 days', '11-15 days', '16-20 days',
                   '21-25 days', '26-30 days', '30+ days']
        return np.select(conditions, choices, default=None)
    
    approved['aging_bucket'] = assign_buckets(approved['aging_days'])
    handover['aging_bucket'] = assign_buckets(handover['aging_days'])
    
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
    pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
    qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
    qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']
    
    return {
        'approved': approved, 'handover': handover, 'pk_zone': pk_zone,
        'qc_center': qc_center, 'pk_normal': pk_normal, 'pk_ai': pk_ai,
        'qc_normal': qc_normal, 'qc_ai': qc_ai
    }

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                '6-7 days', '8-10 days', '11-15 days', '16-20 days', 
                '21-25 days', '26-30 days', '30+ days']

VENDOR_ACTION_OPTIONS = ['--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']

DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
                'logistics_partner_name', 'aging_days', 'aging_bucket']

try:
    with st.spinner('Loading...'):
        df = load_data()
        data = process_data(df)
    
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
        
        # BIG Title with Better Icon
        st.markdown("""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span class="title-icon">⚡</span>
                    <span class="main-title">G-Ops Backlog Dashboard</span>
                </div>
                <p class="subtitle">📊 Real-time Operations Monitoring | Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Summary Metrics - WHITE CARDS
        col1, col2, col3, col4 = st.columns(4)
        for col, label, value in [(col1, "Total Approved", len(approved)), (col2, "PK Zone", len(pk_zone)), 
                                   (col3, "QC Center", len(qc_center)), (col4, "Handover", len(handover))]:
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value:,}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Handover + PK Zone + QC Center
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="section-header">🚚 Handover</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="info-card"><div class="info-title">To Logistics</div><div class="info-value">{len(handover):,}</div></div>', unsafe_allow_html=True)
            st.write("")
            if st.button("View", key="v_handover", use_container_width=True):
                st.session_state.page = 'handover'
                st.rerun()
        
        with col2:
            st.markdown('<div class="section-header">📍 PK Zone</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Normal</div><div class="metric-value">{len(pk_normal):,}</div></div>', unsafe_allow_html=True)
                if st.button("View", key="v_pk_n", use_container_width=True):
                    st.session_state.page = 'pk_normal'
                    st.rerun()
            with c2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">AI</div><div class="metric-value">{len(pk_ai):,}</div></div>', unsafe_allow_html=True)
                if st.button("View", key="v_pk_a", use_container_width=True):
                    st.session_state.page = 'pk_ai'
                    st.rerun()
        
        with col3:
            st.markdown('<div class="section-header">🏢 QC Center</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Normal</div><div class="metric-value">{len(qc_normal):,}</div></div>', unsafe_allow_html=True)
                if st.button("View", key="v_qc_n", use_container_width=True):
                    st.session_state.page = 'qc_normal'
                    st.rerun()
            with c2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">AI</div><div class="metric-value">{len(qc_ai):,}</div></div>', unsafe_allow_html=True)
                if st.button("View", key="v_qc_a", use_container_width=True):
                    st.session_state.page = 'qc_ai'
                    st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ AGING PIVOT TABLES ============
        st.markdown('<div class="section-header">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2, col3 = st.columns(3)
        
        # PK Zone Aging
        with col1:
            st.markdown("**📍 PK Zone**")
            for bucket in BUCKET_ORDER:
                count = pk_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.7rem;color:#b0b0b0;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"pk_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK Zone'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.7rem;color:#505050;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.75rem;font-weight:700;color:#e0e0e0;'>Total: {len(pk_normal):,}</span>", unsafe_allow_html=True)
        
        # QC Center Aging
        with col2:
            st.markdown("**🏢 QC Center**")
            for bucket in BUCKET_ORDER:
                count = qc_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.7rem;color:#b0b0b0;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"qc_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK QC Center'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.7rem;color:#505050;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.75rem;font-weight:700;color:#e0e0e0;'>Total: {len(qc_normal):,}</span>", unsafe_allow_html=True)
        
        # Handover Aging
        with col3:
            st.markdown("**🚚 Handover**")
            for bucket in BUCKET_ORDER:
                count = handover_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.7rem;color:#b0b0b0;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"ho_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'handover_aging_detail'
                            st.session_state.handover_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.7rem;color:#505050;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.75rem;font-weight:700;color:#e0e0e0;'>Total: {len(handover):,}</span>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ PK ZONE VENDOR TABLE ============
        st.markdown('<div class="section-header">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
        
        pk_vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        pk_vendor_counts.columns = ['Vendor', 'Orders']
        
        # Header
        h1, h2, h3 = st.columns([5, 1, 2])
        with h1:
            st.markdown("<span class='table-header'>Vendor</span>", unsafe_allow_html=True)
        with h2:
            st.markdown("<span class='table-header'>Qty</span>", unsafe_allow_html=True)
        with h3:
            st.markdown("<span class='table-header'>Comment</span>", unsafe_allow_html=True)
        
        for i, (_, row) in enumerate(pk_vendor_counts.iterrows()):
            vendor_key = f"pk_{row['Vendor']}"
            c1, c2, c3 = st.columns([5, 1, 2])
            with c1:
                v_name = row['Vendor'][:35] + "..." if len(str(row['Vendor'])) > 35 else row['Vendor']
                st.markdown(f"<span style='font-size:0.7rem;color:#c0c0c0;'>{v_name}</span>", unsafe_allow_html=True)
            with c2:
                if st.button(f"{row['Orders']}", key=f"pv_{i}", use_container_width=True):
                    st.session_state.page = 'vendor_detail'
                    st.session_state.vendor_name = row['Vendor']
                    st.session_state.vendor_zone = 'PK Zone'
                    st.rerun()
            with c3:
                current = st.session_state.vendor_comments.get(vendor_key, '--')
                try:
                    idx = VENDOR_ACTION_OPTIONS.index(current)
                except:
                    idx = 0
                sel = st.selectbox("", VENDOR_ACTION_OPTIONS, index=idx, key=f"pa_{i}", label_visibility="collapsed")
                if sel == '❌ Remove':
                    if vendor_key in st.session_state.vendor_comments:
                        del st.session_state.vendor_comments[vendor_key]
                elif sel != '--':
                    st.session_state.vendor_comments[vendor_key] = sel
        
        st.markdown(f"<span style='font-size:0.75rem;color:#909090;'>{len(pk_vendor_counts)} vendors | {len(pk_normal):,} orders</span>", unsafe_allow_html=True)

    # ==================== DETAIL PAGES ====================
    else:
        if st.button("← Back", key="back"):
            st.session_state.page = 'home'
            st.rerun()
        
        page = st.session_state.page
        
        if page == 'handover':
            title, data_view = "🚚 Handover Orders", handover
        elif page == 'pk_normal':
            title, data_view = "📍 PK Zone - Normal", pk_normal
        elif page == 'pk_ai':
            title, data_view = "📍 PK Zone - AI", pk_ai
        elif page == 'qc_normal':
            title, data_view = "🏢 QC Center - Normal", qc_normal
        elif page == 'qc_ai':
            title, data_view = "🏢 QC Center - AI", qc_ai
        elif page == 'aging_detail':
            zone, bucket = st.session_state.aging_zone, st.session_state.aging_bucket
            icon = "📍" if zone == 'PK Zone' else "🏢"
            title = f"{icon} {zone} - {bucket}"
            data_view = pk_normal[pk_normal['aging_bucket'] == bucket] if zone == 'PK Zone' else qc_normal[qc_normal['aging_bucket'] == bucket]
        elif page == 'vendor_detail':
            vendor, zone = st.session_state.vendor_name, st.session_state.vendor_zone
            title = f"📍 {vendor[:30]}"
            data_view = pk_normal[pk_normal['vendor'] == vendor] if zone == 'PK Zone' else qc_normal[qc_normal['vendor'] == vendor]
        elif page == 'handover_aging_detail':
            bucket = st.session_state.handover_bucket
            title = f"🚚 Handover - {bucket}"
            data_view = handover[handover['aging_bucket'] == bucket]
        else:
            title, data_view = "📋 Orders", approved
        
        st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">{len(data_view):,} orders</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            search = st.text_input("🔍", placeholder="Search...")
        with col2:
            countries = ['All'] + sorted(data_view['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍", countries)
        with col3:
            st.download_button("📥 CSV", data_view.to_csv(index=False), "orders.csv", use_container_width=True)
        
        filtered = data_view.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['vendor'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.dataframe(filtered[[c for c in DISPLAY_COLS if c in filtered.columns]], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error: {e}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
