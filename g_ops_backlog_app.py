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
    # DARK COHESIVE THEME WITH COLORFUL SECTIONS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        background-color: #0d0d0d;
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* ============ VERY BIG TITLE ============ */
    .main-title-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 8px;
    }
    
    .title-icon {
        font-size: 4.5rem;
        filter: drop-shadow(0 4px 20px rgba(255,200,0,0.5));
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 50%, #b0b0b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -2px;
        line-height: 1.1;
    }
    
    .subtitle {
        color: #666666;
        font-size: 1rem;
        margin-top: 10px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* ============ SECTION HEADERS - Different Colors ============ */
    .section-header-orange {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F59E0B;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #F59E0B33;
    }
    
    .section-header-cyan {
        font-size: 1.3rem;
        font-weight: 700;
        color: #06B6D4;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #06B6D433;
    }
    
    .section-header-pink {
        font-size: 1.3rem;
        font-weight: 700;
        color: #EC4899;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #EC489933;
    }
    
    .section-header-lime {
        font-size: 1.3rem;
        font-weight: 700;
        color: #84CC16;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #84CC1633;
    }
    
    .section-header-violet {
        font-size: 1.3rem;
        font-weight: 700;
        color: #8B5CF6;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #8B5CF633;
    }
    
    /* ============ TOP 4 METRIC CARDS - Gradient Backgrounds ============ */
    
    /* Total Approved - Blue Gradient */
    .metric-card-blue {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
        border-radius: 16px;
        padding: 25px 20px;
        box-shadow: 0 8px 32px rgba(59,130,246,0.2);
        border: 1px solid #3B82F633;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card-blue:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(59,130,246,0.35);
    }
    .metric-card-blue .metric-value { color: #60A5FA; }
    .metric-card-blue .metric-label { color: #93C5FD; }
    
    /* PK Zone - Green Gradient */
    .metric-card-green {
        background: linear-gradient(135deg, #134e4a 0%, #0d1f1e 100%);
        border-radius: 16px;
        padding: 25px 20px;
        box-shadow: 0 8px 32px rgba(16,185,129,0.2);
        border: 1px solid #10B98133;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card-green:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(16,185,129,0.35);
    }
    .metric-card-green .metric-value { color: #34D399; }
    .metric-card-green .metric-label { color: #6EE7B7; }
    
    /* QC Center - Purple Gradient */
    .metric-card-purple {
        background: linear-gradient(135deg, #3b2066 0%, #1a0d2e 100%);
        border-radius: 16px;
        padding: 25px 20px;
        box-shadow: 0 8px 32px rgba(139,92,246,0.2);
        border: 1px solid #8B5CF633;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card-purple:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(139,92,246,0.35);
    }
    .metric-card-purple .metric-value { color: #A78BFA; }
    .metric-card-purple .metric-label { color: #C4B5FD; }
    
    /* Handover - Orange Gradient */
    .metric-card-orange {
        background: linear-gradient(135deg, #78350f 0%, #2e1505 100%);
        border-radius: 16px;
        padding: 25px 20px;
        box-shadow: 0 8px 32px rgba(245,158,11,0.2);
        border: 1px solid #F59E0B33;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card-orange:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(245,158,11,0.35);
    }
    .metric-card-orange .metric-value { color: #FBBF24; }
    .metric-card-orange .metric-label { color: #FCD34D; }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
    }
    
    /* ============ 3RD ROW CARDS - Different Colors ============ */
    
    /* Handover Card - Amber/Orange */
    .handover-card {
        background: linear-gradient(145deg, #451a03 0%, #27170a 100%);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 6px 25px rgba(245,158,11,0.15);
        border-left: 5px solid #F59E0B;
        border-top: 1px solid #F59E0B22;
        border-right: 1px solid #F59E0B22;
        border-bottom: 1px solid #F59E0B22;
    }
    .handover-card .info-title { color: #FCD34D; }
    .handover-card .info-value { color: #FBBF24; font-size: 2rem; font-weight: 800; }
    
    /* PK Zone Cards - Cyan/Teal */
    .pk-zone-card {
        background: linear-gradient(145deg, #083344 0%, #0a1a1f 100%);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 6px 25px rgba(6,182,212,0.15);
        border: 1px solid #06B6D433;
        text-align: center;
        transition: all 0.3s ease;
    }
    .pk-zone-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(6,182,212,0.25);
    }
    .pk-zone-card .metric-label { color: #67E8F9; font-size: 0.7rem; }
    .pk-zone-card .metric-value { color: #22D3EE; font-size: 1.8rem; }
    
    /* QC Center Cards - Pink/Rose */
    .qc-center-card {
        background: linear-gradient(145deg, #500724 0%, #1f0a12 100%);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 6px 25px rgba(236,72,153,0.15);
        border: 1px solid #EC489933;
        text-align: center;
        transition: all 0.3s ease;
    }
    .qc-center-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(236,72,153,0.25);
    }
    .qc-center-card .metric-label { color: #F9A8D4; font-size: 0.7rem; }
    .qc-center-card .metric-value { color: #F472B6; font-size: 1.8rem; }
    
    /* ============ AGING SECTION - Lime/Green Theme ============ */
    .aging-container {
        background: linear-gradient(145deg, #1a2e05 0%, #0d1a02 100%);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 6px 25px rgba(132,204,22,0.1);
        border: 1px solid #84CC1633;
        margin-bottom: 15px;
    }
    
    .aging-title {
        font-size: 1rem;
        font-weight: 700;
        color: #BEF264;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #84CC1633;
    }
    
    .aging-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #84CC1611;
    }
    
    .aging-bucket { color: #A3E635; font-size: 0.8rem; }
    .aging-count { color: #D9F99D; font-weight: 600; }
    .aging-total { color: #84CC16; font-weight: 700; font-size: 0.9rem; margin-top: 10px; }
    
    /* ============ VENDOR SECTION - Violet/Purple Theme ============ */
    .vendor-container {
        background: linear-gradient(145deg, #2e1065 0%, #1a0a3e 100%);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 6px 25px rgba(139,92,246,0.1);
        border: 1px solid #8B5CF633;
    }
    
    .vendor-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #C4B5FD;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding-bottom: 12px;
        border-bottom: 1px solid #8B5CF633;
        margin-bottom: 10px;
    }
    
    .vendor-row {
        padding: 8px 0;
        border-bottom: 1px solid #8B5CF622;
    }
    
    .vendor-name { color: #DDD6FE; font-size: 0.8rem; }
    .vendor-count { color: #A78BFA; font-weight: 600; }
    .vendor-total { color: #8B5CF6; font-weight: 700; font-size: 0.85rem; margin-top: 12px; }
    
    /* ============ BUTTONS - Styled per section ============ */
    .stButton > button {
        background: linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 100%) !important;
        color: #a0a0a0 !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        transition: all 0.3s ease !important;
        min-height: 36px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, #3a3a3a 0%, #2a2a2a 100%) !important;
        color: #ffffff !important;
        border-color: #555555 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    /* ============ DROPDOWN - Dark Style ============ */
    .stSelectbox > div > div {
        background: #1a1a2e !important;
        border: 1px solid #8B5CF644 !important;
        border-radius: 8px !important;
        color: #DDD6FE !important;
        font-size: 0.8rem !important;
        min-height: 36px !important;
    }
    
    .stSelectbox label {
        color: #A78BFA !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #333333;
        margin: 30px 0;
    }
    
    /* Text Colors */
    .stMarkdown, p, span, label { color: #a0a0a0 !important; font-size: 0.85rem !important; }
    h1, h2, h3, h4, h5, h6 { color: #e0e0e0 !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0d0d0d; }
    ::-webkit-scrollbar-thumb { background: #444444; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #555555; }
    
    </style>
    """, unsafe_allow_html=True)
else:
    # DARK THEME for Detail Pages
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 5px;
    }
    
    .page-subtitle {
        color: #888888;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 100%) !important;
        color: #60a5fa !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #3B82F6 !important;
        color: #ffffff !important;
        border-color: #3B82F6 !important;
    }
    
    .stTextInput > div > div > input {
        background: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 0.85rem !important;
    }
    
    .stSelectbox > div > div {
        background: #1a1a1a !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
    }
    
    .stSelectbox label, .stTextInput label {
        color: #888888 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stDataFrame"] {
        background: #111111;
        border-radius: 12px;
        border: 1px solid #333333;
    }
    
    p, span, label, .stMarkdown { color: #c0c0c0 !important; font-size: 0.85rem !important; }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0d0d0d; }
    ::-webkit-scrollbar-thumb { background: #444444; border-radius: 4px; }
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
        
        # ============ VERY BIG TITLE ============
        st.markdown("""
            <div style="margin-bottom: 25px;">
                <div class="main-title-container">
                    <span class="title-icon">⚡</span>
                    <span class="main-title">G-Ops Backlog Dashboard</span>
                </div>
                <p class="subtitle">📊 Real-time Operations Monitoring &nbsp;|&nbsp; Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ TOP 4 METRIC CARDS - Gradient Backgrounds ============
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
                <div class="metric-card-blue">
                    <div class="metric-label">Total Approved</div>
                    <div class="metric-value">{len(approved):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card-green">
                    <div class="metric-label">PK Zone</div>
                    <div class="metric-value">{len(pk_zone):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card-purple">
                    <div class="metric-label">QC Center</div>
                    <div class="metric-value">{len(qc_center):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="metric-card-orange">
                    <div class="metric-label">Handover</div>
                    <div class="metric-value">{len(handover):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ 3RD ROW: HANDOVER + PK ZONE + QC CENTER ============
        col1, col2, col3 = st.columns(3)
        
        # Handover - Orange Theme
        with col1:
            st.markdown('<div class="section-header-orange">🚚 Handover</div>', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="handover-card">
                    <div class="info-title">To Logistics Partner</div>
                    <div class="info-value">{len(handover):,}</div>
                </div>
            ''', unsafe_allow_html=True)
            st.write("")
            if st.button("View Details", key="v_handover", use_container_width=True):
                st.session_state.page = 'handover'
                st.rerun()
        
        # PK Zone - Cyan Theme
        with col2:
            st.markdown('<div class="section-header-cyan">📍 PK Zone</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'''
                    <div class="pk-zone-card">
                        <div class="metric-label">Normal</div>
                        <div class="metric-value">{len(pk_normal):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_pk_n", use_container_width=True):
                    st.session_state.page = 'pk_normal'
                    st.rerun()
            with c2:
                st.markdown(f'''
                    <div class="pk-zone-card">
                        <div class="metric-label">AI Orders</div>
                        <div class="metric-value">{len(pk_ai):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_pk_a", use_container_width=True):
                    st.session_state.page = 'pk_ai'
                    st.rerun()
        
        # QC Center - Pink Theme
        with col3:
            st.markdown('<div class="section-header-pink">🏢 QC Center</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'''
                    <div class="qc-center-card">
                        <div class="metric-label">Normal</div>
                        <div class="metric-value">{len(qc_normal):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_qc_n", use_container_width=True):
                    st.session_state.page = 'qc_normal'
                    st.rerun()
            with c2:
                st.markdown(f'''
                    <div class="qc-center-card">
                        <div class="metric-label">AI Orders</div>
                        <div class="metric-value">{len(qc_ai):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_qc_a", use_container_width=True):
                    st.session_state.page = 'qc_ai'
                    st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ AGING ANALYSIS - Lime/Green Theme ============
        st.markdown('<div class="section-header-lime">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2, col3 = st.columns(3)
        
        # PK Zone Aging
        with col1:
            st.markdown('<div class="aging-title">📍 PK Zone</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = pk_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.8rem;color:#A3E635;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"pk_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK Zone'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.8rem;color:#3f6212;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<p class='aging-total'>Total: {len(pk_normal):,}</p>", unsafe_allow_html=True)
        
        # QC Center Aging
        with col2:
            st.markdown('<div class="aging-title">🏢 QC Center</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = qc_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.8rem;color:#A3E635;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"qc_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK QC Center'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.8rem;color:#3f6212;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<p class='aging-total'>Total: {len(qc_normal):,}</p>", unsafe_allow_html=True)
        
        # Handover Aging
        with col3:
            st.markdown('<div class="aging-title">🚚 Handover</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = handover_aging.get(bucket, 0)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span style='font-size:0.8rem;color:#A3E635;'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"ho_a_{bucket}", use_container_width=True):
                            st.session_state.page = 'handover_aging_detail'
                            st.session_state.handover_bucket = bucket
                            st.rerun()
                    else:
                        st.markdown("<span style='font-size:0.8rem;color:#3f6212;'>0</span>", unsafe_allow_html=True)
            st.markdown(f"<p class='aging-total'>Total: {len(handover):,}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ PK ZONE VENDOR TABLE - Violet/Purple Theme ============
        st.markdown('<div class="section-header-violet">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
        
        pk_vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        pk_vendor_counts.columns = ['Vendor', 'Orders']
        
        # Header
        h1, h2, h3 = st.columns([5, 1, 2])
        with h1:
            st.markdown("<span class='vendor-header'>Vendor Name</span>", unsafe_allow_html=True)
        with h2:
            st.markdown("<span class='vendor-header'>Qty</span>", unsafe_allow_html=True)
        with h3:
            st.markdown("<span class='vendor-header'>Comment</span>", unsafe_allow_html=True)
        
        for i, (_, row) in enumerate(pk_vendor_counts.iterrows()):
            vendor_key = f"pk_{row['Vendor']}"
            c1, c2, c3 = st.columns([5, 1, 2])
            with c1:
                v_name = row['Vendor'][:35] + "..." if len(str(row['Vendor'])) > 35 else row['Vendor']
                st.markdown(f"<span class='vendor-name'>{v_name}</span>", unsafe_allow_html=True)
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
        
        st.markdown(f"<p class='vendor-total'>{len(pk_vendor_counts)} vendors &nbsp;|&nbsp; {len(pk_normal):,} total orders</p>", unsafe_allow_html=True)

    # ==================== DETAIL PAGES ====================
    else:
        if st.button("← Back to Dashboard", key="back"):
            st.session_state.page = 'home'
            st.rerun()
        
        page = st.session_state.page
        
        if page == 'handover':
            title, data_view = "🚚 Handover Orders", handover
        elif page == 'pk_normal':
            title, data_view = "📍 PK Zone - Normal Orders", pk_normal
        elif page == 'pk_ai':
            title, data_view = "📍 PK Zone - AI Orders", pk_ai
        elif page == 'qc_normal':
            title, data_view = "🏢 QC Center - Normal Orders", qc_normal
        elif page == 'qc_ai':
            title, data_view = "🏢 QC Center - AI Orders", qc_ai
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
        st.markdown(f'<div class="page-subtitle">{len(data_view):,} orders found</div>', unsafe_allow_html=True)
        
        st.write("")
        
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order, Customer or Vendor...")
        with col2:
            countries = ['All Countries'] + sorted(data_view['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Filter by Country", countries)
        with col3:
            st.write("")
            st.download_button("📥 Export CSV", data_view.to_csv(index=False), "orders.csv", use_container_width=True)
        
        filtered = data_view.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['vendor'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All Countries':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.dataframe(filtered[[c for c in DISPLAY_COLS if c in filtered.columns]], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error: {e}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
