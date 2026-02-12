import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

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

# Custom CSS - STRONG OVERRIDE
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* ============ MAIN BACKGROUND - DARK GRADIENT - FORCED ============ */
.stApp, 
[data-testid="stAppViewContainer"],
.main,
.block-container,
[data-testid="stAppViewBlockContainer"] {
    background: linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
    background-color: #0d0d0d !important;
}

html, body, .stApp > header {
    background: #0d0d0d !important;
}

[data-testid="stHeader"] { 
    background: transparent !important; 
    background-color: transparent !important;
}

#MainMenu, footer, header { visibility: hidden !important; }

/* ============ SIDEBAR STYLING - FORCED VISIBILITY ============ */
[data-testid="stSidebar"],
section[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
[data-testid="stSidebar"] > div > div > div {
    background: linear-gradient(180deg, #151515 0%, #0a0a0a 100%) !important;
    background-color: #0f0f0f !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #2a2a2a !important;
    min-width: 300px !important;
    width: 300px !important;
}

[data-testid="stSidebarContent"] {
    background: linear-gradient(180deg, #151515 0%, #0a0a0a 100%) !important;
    background-color: #0f0f0f !important;
    padding: 20px 15px !important;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(145deg, #252525 0%, #1a1a1a 100%) !important;
    color: #d0d0d0 !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
    margin-bottom: 6px !important;
    text-align: left !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(145deg, #3a3a3a 0%, #2a2a2a 100%) !important;
    border-color: #4a4a4a !important;
    transform: translateX(5px) !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #3a3a3a !important;
    color: #d0d0d0 !important;
}

/* ============ HUGE TITLE - BIGGER ============ */
.main-title-box {
    padding: 30px 0;
    margin-bottom: 20px;
}

.title-row {
    display: flex;
    align-items: center;
    gap: 25px;
}

.title-icon-huge {
    font-size: 6rem !important;
    line-height: 1;
    filter: drop-shadow(0 8px 30px rgba(255,200,0,0.7));
    animation: pulse-big 2s ease-in-out infinite;
}

@keyframes pulse-big {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}

.main-title-huge {
    font-size: 5.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 40%, #d0d0d0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    padding: 0 !important;
    letter-spacing: -4px !important;
    line-height: 1 !important;
    text-shadow: none;
}

.subtitle-text {
    color: #666666 !important;
    font-size: 1.2rem !important;
    margin-top: 15px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

/* ============ TOP 4 METRIC CARDS - WHITE with BLACK TEXT ============ */
.metric-card-white {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 28px 20px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}
.metric-card-white:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
}
.metric-card-white .metric-label {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: #444444 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    margin-bottom: 10px !important;
}
.metric-card-white .metric-value {
    font-size: 3rem !important;
    font-weight: 900 !important;
    color: #111111 !important;
}

/* ============ SECTION HEADERS - WHITE ============ */
.section-header-white {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    margin: 25px 0 18px 0 !important;
    padding-bottom: 12px !important;
    border-bottom: 2px solid #333333 !important;
}

/* ============ HANDOVER CARD - DARK BROWN ============ */
.handover-card {
    background: linear-gradient(145deg, #4a2c17 0%, #2d1a0e 100%) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 8px 30px rgba(74,44,23,0.5) !important;
    border: 1px solid #5c3a22 !important;
}
.handover-card .info-title {
    color: #ffffff !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    margin-bottom: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.handover-card .info-value {
    color: #ffffff !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
}

/* ============ PK ZONE & QC CENTER CARDS - LIGHT GREEN SHADED ============ */
.green-card {
    background: linear-gradient(145deg, #1f4d1f 0%, #143314 100%) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    box-shadow: 0 6px 25px rgba(34,197,94,0.2) !important;
    border: 1px solid #2d6a2d !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}
.green-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 35px rgba(34,197,94,0.3) !important;
}
.green-card .metric-label {
    color: #ffffff !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    margin-bottom: 10px !important;
}
.green-card .metric-value {
    color: #7eed9e !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

/* ============ AGING SECTION STYLING ============ */
.aging-section-title {
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    margin-bottom: 15px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid #333333 !important;
}

.aging-bucket-text {
    color: #b0b0b0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ============ GRAY BUTTONS ============ */
.stButton > button {
    background: #4a4a4a !important;
    color: #e0e0e0 !important;
    border: 1px solid #5a5a5a !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
    min-height: 36px !important;
}

.stButton > button:hover {
    background: #5a5a5a !important;
    color: #ffffff !important;
    border-color: #6a6a6a !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
}

/* ============ VENDOR TABLE STYLING ============ */
.vendor-header {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    color: #888888 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    padding-bottom: 15px !important;
    border-bottom: 1px solid #3a3a3a !important;
    margin-bottom: 10px !important;
}

.vendor-name-text {
    color: #c0c0c0 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ============ DROPDOWN - GRAY ============ */
.stSelectbox > div > div {
    background: #4a4a4a !important;
    border: 1px solid #5a5a5a !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
    font-size: 0.85rem !important;
    min-height: 36px !important;
}

.stSelectbox label {
    color: #888888 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid #333333 !important;
    margin: 30px 0 !important;
}

/* Text Colors */
.stMarkdown, p, span, label { color: #a0a0a0 !important; font-size: 0.9rem !important; }
h1, h2, h3, h4, h5, h6 { color: #e0e0e0 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #444444; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #555555; }

/* ============ DETAIL PAGE STYLING ============ */
.page-title {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin-bottom: 8px !important;
}

.page-subtitle {
    color: #888888 !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > input {
    background: #1a1a1a !important;
    color: #e0e0e0 !important;
    border: 1px solid #404040 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-size: 0.9rem !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
}

[data-testid="stDataFrame"] {
    background: #111111 !important;
    border-radius: 14px !important;
    border: 1px solid #333333 !important;
}

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
    with st.spinner('Loading data...'):
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

    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown("## 🎯 Quick Navigation")
        st.markdown("---")
        
        # Home Button
        if st.button("🏠 Dashboard Home", key="sb_home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        # Handover Section
        st.markdown('<p style="color:#F59E0B;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:25px 0 12px 0;padding-bottom:8px;border-bottom:1px solid #333;">🚚 Handover</p>', unsafe_allow_html=True)
        if st.button(f"📦 All Handover Orders ({len(handover):,})", key="sb_handover", use_container_width=True):
            st.session_state.page = 'handover'
            st.rerun()
        
        # PK Zone Section
        st.markdown('<p style="color:#22C55E;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:25px 0 12px 0;padding-bottom:8px;border-bottom:1px solid #333;">📍 PK Zone</p>', unsafe_allow_html=True)
        if st.button(f"📋 Normal Orders ({len(pk_normal):,})", key="sb_pk_normal", use_container_width=True):
            st.session_state.page = 'pk_normal'
            st.rerun()
        if st.button(f"🤖 AI Orders ({len(pk_ai):,})", key="sb_pk_ai", use_container_width=True):
            st.session_state.page = 'pk_ai'
            st.rerun()
        
        # QC Center Section
        st.markdown('<p style="color:#22C55E;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:25px 0 12px 0;padding-bottom:8px;border-bottom:1px solid #333;">🏢 QC Center</p>', unsafe_allow_html=True)
        if st.button(f"📋 Normal Orders ({len(qc_normal):,})", key="sb_qc_normal", use_container_width=True):
            st.session_state.page = 'qc_normal'
            st.rerun()
        if st.button(f"🤖 AI Orders ({len(qc_ai):,})", key="sb_qc_ai", use_container_width=True):
            st.session_state.page = 'qc_ai'
            st.rerun()
        
        # Aging Analysis Section
        st.markdown('<p style="color:#60A5FA;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:25px 0 12px 0;padding-bottom:8px;border-bottom:1px solid #333;">📊 Aging Analysis</p>', unsafe_allow_html=True)
        
        # PK Zone Aging Dropdown
        pk_aging_data = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        pk_aging_options = ["Select PK Zone Aging..."] + [f"{b} ({pk_aging_data.get(b, 0)})" for b in BUCKET_ORDER if pk_aging_data.get(b, 0) > 0]
        selected_pk = st.selectbox("PK Zone", pk_aging_options, key="sb_pk_aging_dd", label_visibility="collapsed")
        if selected_pk != "Select PK Zone Aging...":
            bucket = selected_pk.split(" (")[0]
            st.session_state.page = 'aging_detail'
            st.session_state.aging_zone = 'PK Zone'
            st.session_state.aging_bucket = bucket
            st.rerun()
        
        # QC Center Aging Dropdown
        qc_aging_data = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging_options = ["Select QC Center Aging..."] + [f"{b} ({qc_aging_data.get(b, 0)})" for b in BUCKET_ORDER if qc_aging_data.get(b, 0) > 0]
        selected_qc = st.selectbox("QC Center", qc_aging_options, key="sb_qc_aging_dd", label_visibility="collapsed")
        if selected_qc != "Select QC Center Aging...":
            bucket = selected_qc.split(" (")[0]
            st.session_state.page = 'aging_detail'
            st.session_state.aging_zone = 'PK QC Center'
            st.session_state.aging_bucket = bucket
            st.rerun()
        
        # Handover Aging Dropdown
        ho_aging_data = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        ho_aging_options = ["Select Handover Aging..."] + [f"{b} ({ho_aging_data.get(b, 0)})" for b in BUCKET_ORDER if ho_aging_data.get(b, 0) > 0]
        selected_ho = st.selectbox("Handover", ho_aging_options, key="sb_ho_aging_dd", label_visibility="collapsed")
        if selected_ho != "Select Handover Aging...":
            bucket = selected_ho.split(" (")[0]
            st.session_state.page = 'handover_aging_detail'
            st.session_state.handover_bucket = bucket
            st.rerun()

    # ==================== HOME PAGE ====================
    if st.session_state.page == 'home':
        
        # ============ HUGE TITLE - MUCH BIGGER NOW ============
        st.markdown("""
            <div class="main-title-box">
                <div class="title-row">
                    <span class="title-icon-huge">⚡</span>
                    <span class="main-title-huge">G-Ops Backlog Dashboard</span>
                </div>
                <p class="subtitle-text">📊 Real-time Operations Monitoring &nbsp;|&nbsp; Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ TOP 4 METRIC CARDS - WHITE with BLACK TEXT ============
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
                <div class="metric-card-white">
                    <div class="metric-label">Total Approved</div>
                    <div class="metric-value">{len(approved):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
                <div class="metric-card-white">
                    <div class="metric-label">PK Zone</div>
                    <div class="metric-value">{len(pk_zone):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card-white">
                    <div class="metric-label">QC Center</div>
                    <div class="metric-value">{len(qc_center):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="metric-card-white">
                    <div class="metric-label">Handover</div>
                    <div class="metric-value">{len(handover):,}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ 3RD ROW: HANDOVER + PK ZONE + QC CENTER ============
        col1, col2, col3 = st.columns(3)
        
        # Handover - Dark Brown
        with col1:
            st.markdown('<div class="section-header-white">🚚 Handover</div>', unsafe_allow_html=True)
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
        
        # PK Zone - Light Green
        with col2:
            st.markdown('<div class="section-header-white">📍 PK Zone</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'''
                    <div class="green-card">
                        <div class="metric-label">Normal</div>
                        <div class="metric-value">{len(pk_normal):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_pk_n", use_container_width=True):
                    st.session_state.page = 'pk_normal'
                    st.rerun()
            with c2:
                st.markdown(f'''
                    <div class="green-card">
                        <div class="metric-label">AI Orders</div>
                        <div class="metric-value">{len(pk_ai):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_pk_a", use_container_width=True):
                    st.session_state.page = 'pk_ai'
                    st.rerun()
        
        # QC Center - Light Green
        with col3:
            st.markdown('<div class="section-header-white">🏢 QC Center</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'''
                    <div class="green-card">
                        <div class="metric-label">Normal</div>
                        <div class="metric-value">{len(qc_normal):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_qc_n", use_container_width=True):
                    st.session_state.page = 'qc_normal'
                    st.rerun()
            with c2:
                st.markdown(f'''
                    <div class="green-card">
                        <div class="metric-label">AI Orders</div>
                        <div class="metric-value">{len(qc_ai):,}</div>
                    </div>
                ''', unsafe_allow_html=True)
                if st.button("View", key="v_qc_a", use_container_width=True):
                    st.session_state.page = 'qc_ai'
                    st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ AGING ANALYSIS - WHITE HEADING ============
        st.markdown('<div class="section-header-white">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2, col3 = st.columns(3)
        
        # PK Zone Aging
        with col1:
            st.markdown('<div class="aging-section-title">📍 PK ZONE</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = pk_aging.get(bucket, 0)
                st.markdown(f"<div style='border-bottom:1px solid #222;'></div>", unsafe_allow_html=True)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if st.button(f"{count}", key=f"pk_a_{bucket}", use_container_width=True):
                        if count > 0:
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK Zone'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
            st.markdown(f"<p style='color:#ffffff;font-weight:800;font-size:1rem;margin-top:15px;'>Total: {len(pk_normal):,}</p>", unsafe_allow_html=True)
        
        # QC Center Aging
        with col2:
            st.markdown('<div class="aging-section-title">🏢 QC CENTER</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = qc_aging.get(bucket, 0)
                st.markdown(f"<div style='border-bottom:1px solid #222;'></div>", unsafe_allow_html=True)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if st.button(f"{count}", key=f"qc_a_{bucket}", use_container_width=True):
                        if count > 0:
                            st.session_state.page = 'aging_detail'
                            st.session_state.aging_zone = 'PK QC Center'
                            st.session_state.aging_bucket = bucket
                            st.rerun()
            st.markdown(f"<p style='color:#ffffff;font-weight:800;font-size:1rem;margin-top:15px;'>Total: {len(qc_normal):,}</p>", unsafe_allow_html=True)
        
        # Handover Aging
        with col3:
            st.markdown('<div class="aging-section-title">🚚 HANDOVER</div>', unsafe_allow_html=True)
            for bucket in BUCKET_ORDER:
                count = handover_aging.get(bucket, 0)
                st.markdown(f"<div style='border-bottom:1px solid #222;'></div>", unsafe_allow_html=True)
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                with c2:
                    if st.button(f"{count}", key=f"ho_a_{bucket}", use_container_width=True):
                        if count > 0:
                            st.session_state.page = 'handover_aging_detail'
                            st.session_state.handover_bucket = bucket
                            st.rerun()
            st.markdown(f"<p style='color:#ffffff;font-weight:800;font-size:1rem;margin-top:15px;'>Total: {len(handover):,}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ============ PK ZONE VENDOR TABLE ============
        st.markdown('<div class="section-header-white">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
        
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
            
            # Row with thin border
            st.markdown("<div style='border-bottom: 1px solid #2a2a2a;'></div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([5, 1, 2])
            with c1:
                v_name = row['Vendor'][:40] + "..." if len(str(row['Vendor'])) > 40 else row['Vendor']
                st.markdown(f"<span class='vendor-name-text'>{v_name}</span>", unsafe_allow_html=True)
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
        
        st.markdown(f"<p style='color:#888888;font-size:0.9rem;margin-top:20px;'>{len(pk_vendor_counts)} vendors &nbsp;|&nbsp; {len(pk_normal):,} total orders</p>", unsafe_allow_html=True)

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
