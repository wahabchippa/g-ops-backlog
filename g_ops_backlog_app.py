import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

# Page config - NO initial_sidebar_state
st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="⚡", layout="wide")

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_sidebar' not in st.session_state:
    st.session_state.show_sidebar = True
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
if 'search_result_order' not in st.session_state:
    st.session_state.search_result_order = None
if 'search_result_vendor' not in st.session_state:
    st.session_state.search_result_vendor = None

def toggle_sidebar():
    st.session_state.show_sidebar = not st.session_state.show_sidebar

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
}

/* Sidebar toggle button style */
.sidebar-toggle {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 999999;
    background: linear-gradient(145deg, #333 0%, #222 100%);
    border: 1px solid #444;
    border-radius: 8px;
    padding: 8px 16px;
    color: white;
    font-weight: 600;
    cursor: pointer;
}

/* Custom sidebar */
.custom-sidebar {
    background: linear-gradient(180deg, #151515 0%, #0a0a0a 100%);
    border-right: 1px solid #2a2a2a;
    padding: 20px;
    height: 100vh;
    overflow-y: auto;
}

.metric-card-white {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    text-align: center;
    transition: all 0.3s ease;
}
.metric-card-white:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}
.metric-card-white .metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #444444;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}
.metric-card-white .metric-value {
    font-size: 3rem;
    font-weight: 900;
    color: #111111;
}

.section-header-white {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    margin: 25px 0 18px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #333333;
}

.handover-card {
    background: linear-gradient(145deg, #4a2c17 0%, #2d1a0e 100%);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(74,44,23,0.5);
    border: 1px solid #5c3a22;
}
.handover-card .info-title {
    color: #ffffff;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.handover-card .info-value {
    color: #ffffff;
    font-size: 2.8rem;
    font-weight: 900;
}

.green-card {
    background: linear-gradient(145deg, #1f4d1f 0%, #143314 100%);
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 6px 25px rgba(34,197,94,0.2);
    border: 1px solid #2d6a2d;
    text-align: center;
    transition: all 0.3s ease;
}
.green-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 35px rgba(34,197,94,0.3);
}
.green-card .metric-label {
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}
.green-card .metric-value {
    color: #7eed9e;
    font-size: 2.2rem;
    font-weight: 800;
}

.aging-section-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #333333;
}

.aging-bucket-text {
    color: #b0b0b0;
    font-size: 0.85rem;
    font-weight: 500;
}

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
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.vendor-header {
    font-size: 0.8rem;
    font-weight: 700;
    color: #888888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 15px;
    border-bottom: 1px solid #3a3a3a;
    margin-bottom: 10px;
}

.vendor-name-text {
    color: #c0c0c0;
    font-size: 0.85rem;
    font-weight: 500;
}

.stSelectbox > div > div {
    background: #4a4a4a !important;
    border: 1px solid #5a5a5a !important;
    border-radius: 8px !important;
    color: #e0e0e0 !important;
    font-size: 0.85rem !important;
    min-height: 36px !important;
}

hr {
    border: none;
    border-top: 1px solid #333333;
    margin: 30px 0;
}

.stMarkdown, p, span, label { color: #a0a0a0 !important; font-size: 0.9rem !important; }
h1, h2, h3, h4, h5, h6 { color: #e0e0e0 !important; }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #444444; border-radius: 5px; }

/* MAIN HEADER STYLES */
.main-header-container {
    margin-bottom: 25px !important;
}
.main-header-title {
    display: flex !important;
    align-items: center !important;
    gap: 18px !important;
    margin-bottom: 8px !important;
}
.main-header-icon {
    font-size: 48px !important;
    line-height: 1 !important;
}
.main-header-text {
    font-size: 48px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    line-height: 1 !important;
}
.main-header-subtitle {
    color: #666666 !important;
    font-size: 1.1rem !important;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.page-subtitle {
    color: #888888;
    font-size: 1.1rem;
    font-weight: 500;
}

.stTextInput > div > div > input {
    background: #1a1a1a !important;
    color: #e0e0e0 !important;
    border: 1px solid #404040 !important;
    border-radius: 10px !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
}

[data-testid="stDataFrame"] {
    background: #111111;
    border-radius: 14px;
    border: 1px solid #333333;
}

/* SEARCH BOX STYLES */
.search-container {
    background: linear-gradient(145deg, #1a1a1a 0%, #252525 100%);
    border: 2px solid #3a3a3a;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 25px;
}

.search-result-card {
    background: linear-gradient(145deg, #1f1f1f 0%, #2a2a2a 100%);
    border: 1px solid #444;
    border-radius: 12px;
    padding: 20px;
    margin-top: 15px;
}

.search-result-title {
    color: #22C55E;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 15px;
}

.search-result-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #333;
}

.search-label {
    color: #888;
    font-size: 0.85rem;
    font-weight: 600;
}

.search-value {
    color: #fff;
    font-size: 0.9rem;
    font-weight: 500;
}

.vendor-match-card {
    background: linear-gradient(145deg, #2d1f4e 0%, #1a1333 100%);
    border: 1px solid #5c4d7a;
    border-radius: 12px;
    padding: 15px 20px;
    margin-top: 10px;
    cursor: pointer;
}

.vendor-match-name {
    color: #a78bfa;
    font-size: 1rem;
    font-weight: 700;
}

.vendor-match-count {
    color: #c4b5fd;
    font-size: 0.85rem;
}

/* 3PL SUMMARY TABLE STYLES */
.tpl-table-wrapper {
    overflow-x: auto;
    border-radius: 16px;
    border: 1px solid #2a2a2a;
    margin-top: 20px;
}
.tpl-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
}
.tpl-table th {
    background: #1a1a2e;
    color: #a78bfa;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12px 10px;
    border: 1px solid #2a2a3a;
    text-align: center;
    font-size: 0.75rem;
}
.tpl-table th.provider-header {
    background: #0f0f1a;
    color: #e0e0e0;
    text-align: left;
    min-width: 180px;
}
.tpl-table th.day-group {
    background: #111827;
    color: #60a5fa;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #3b82f6;
}
.tpl-table td {
    padding: 10px 10px;
    border: 1px solid #1f1f1f;
    text-align: center;
    color: #c0c0c0;
    font-size: 0.82rem;
}
.tpl-table td.provider-name {
    text-align: left;
    font-weight: 700;
    color: #f0f0f0;
    background: #111111;
    padding-left: 14px;
    font-size: 0.8rem;
    letter-spacing: 0.3px;
}
.tpl-table tr:nth-child(even) td {
    background: #0f0f0f;
}
.tpl-table tr:nth-child(odd) td {
    background: #141414;
}
.tpl-table tr:hover td {
    background: #1c1c2e !important;
}
.tpl-table td.provider-name:hover {
    background: #1c1c2e !important;
}
.tpl-table .total-row td {
    background: #1a1a2e !important;
    color: #7eed9e;
    font-weight: 800;
    border-top: 2px solid #2d6a2d;
}
.tpl-table .total-row td.provider-name {
    color: #7eed9e;
    background: #0f1a0f !important;
}
.tpl-value-highlight {
    color: #ffffff;
    font-weight: 700;
}
.tpl-zero {
    color: #3a3a3a;
}
</style>
""", unsafe_allow_html=True)

# Data Loading
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"
TPL_SHEET_ID = "1V03fqI2tGbY3ImkQaoZGwJ98iyrN4z_GXRKRP023zUY"

@st.cache_data(ttl=600, show_spinner=False)
def load_ai_fleek_ids():
    """Load AI fleek_ids from AI tab"""
    ai_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=AI"
    ai_df = pd.read_csv(ai_url, low_memory=False)
    return set(ai_df['fleek_id'].astype(str).str.strip().tolist())

@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    # Load main data from Extract 1
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Extract%201"
    df = pd.read_csv(url, low_memory=False)
    
    # Load AI fleek_ids
    ai_fleek_ids = load_ai_fleek_ids()
    
    # ===== DERIVE "QC or zone" from is_zone_vendor + vendor_country =====
    def get_qc_zone(row):
        is_zone = str(row.get('is_zone_vendor', '')).strip().upper()
        vendor_country = str(row.get('vendor_country', '')).strip().upper()
        
        if vendor_country == 'PK':
            if is_zone == 'TRUE':
                return 'PK Zone'
            else:
                return 'PK QC Center'
        elif vendor_country == 'IN':
            if is_zone == 'TRUE':
                return 'IN Zone'
            else:
                return 'IN QC Center'
        return 'Other'
    
    df['QC or zone'] = df.apply(get_qc_zone, axis=1)
    
    # ===== DERIVE "Order Type" from AI tab fleek_id list =====
    df['Order Type'] = df['fleek_id'].apply(
        lambda x: 'AI Order' if str(x).strip() in ai_fleek_ids else 'Normal Order'
    )
    
    return df

@st.cache_data(ttl=600, show_spinner=False)
def process_data(df):
    now = datetime.now()
    
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))].copy()
    
    # Parse dates
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return pd.NaT
        date_str = str(date_str).strip()
        for fmt in ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y', '%B %d, %Y, %H:%M', '%Y-%m-%d %H:%M:%S']:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT
    
    approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
    approved['aging_days'] = (now - approved['qc_date']).dt.days
    
    handover['handover_date'] = handover['logistics_partner_handedover_at'].apply(parse_date)
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
    
    all_data = pd.concat([approved, handover], ignore_index=True)
    
    return {
        'approved': approved, 'handover': handover, 'pk_zone': pk_zone,
        'qc_center': qc_center, 'pk_normal': pk_normal, 'pk_ai': pk_ai,
        'qc_normal': qc_normal, 'qc_ai': qc_ai, 'all_data': all_data
    }

# ==================== 3PL DATA LOADING ====================
@st.cache_data(ttl=300, show_spinner=False)
def load_3pl_sheet(sheet_name):
    """Load a single tab from the 3PL Google Sheet using URL-encoded sheet name"""
    encoded_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{TPL_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    try:
        # Load with no header so we get raw rows with positional access
        df = pd.read_csv(url, header=None, low_memory=False)
        return df
    except Exception as e:
        return pd.DataFrame()

# Provider config:
# sheet      = tab name in Google Sheet
# marker     = text in col A that identifies this provider's section header row
# total_marker = text in col A that identifies the TOTAL SUMMARY row for this provider
# day_col_start = 0-indexed column index where Monday's first metric (Orders) starts
# Each day has 5 columns: Orders, Boxes, Weight, <20kg, 20kg+
TPL_PROVIDER_CONFIG = {
    "GLOBAL EXPRESS (QC CENTER)": {
        "sheet": "GE QC Center & Zone",
        "section_marker": "GLOBAL EXPRESS (QC CENTER)",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,   # col B = index 1
    },
    "GLOBAL EXPRESS (ZONES)": {
        "sheet": "GE QC Center & Zone",
        "section_marker": "GLOBAL EXPRESS (ZONES)",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,
    },
    "ECL LOGISTICS (QC CENTER)": {
        "sheet": "ECL QC Center & Zone",
        "section_marker": "ECL LOGISTICS (QC CENTER)",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,
    },
    "ECL LOGISTICS (ZONES)": {
        "sheet": "ECL QC Center & Zone",
        "section_marker": "ECL LOGISTICS (ZONES)",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,
    },
    "KERRY LOGISTICS": {
        "sheet": "Kerry",
        "section_marker": "KERRY LOGISTICS",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,
    },
    "APX EXPRESS": {
        "sheet": "APX",
        "section_marker": "APX EXPRESS",
        "total_marker": "TOTAL SUMMARY",
        "day_col_start": 1,
    },
}

# Which sheets to load (unique)
TPL_PROVIDERS = {k: v["sheet"] for k, v in TPL_PROVIDER_CONFIG.items()}
TPL_SHEETS_NEEDED = list(set(TPL_PROVIDERS.values()))

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
    all_data = data['all_data']

    # ==================== LAYOUT ====================
    if st.session_state.show_sidebar:
        sidebar_col, main_col = st.columns([1, 4])
    else:
        sidebar_col = None
        main_col = st.container()

    # ==================== SIDEBAR ====================
    if st.session_state.show_sidebar and sidebar_col:
        with sidebar_col:
            if st.button("✕ Close Sidebar", key="close_btn", use_container_width=True):
                st.session_state.show_sidebar = False
                st.rerun()
            
            st.markdown("## 🎯 Navigation")
            st.markdown("---")
            
            if st.button("🏠 Dashboard Home", key="sb_home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("🚀 3PL Summary", key="sb_3pl", use_container_width=True):
                st.session_state.page = '3pl_summary'
                st.rerun()
            
            st.markdown('<p style="color:#F59E0B;font-size:0.75rem;font-weight:700;margin:20px 0 10px 0;">🚚 HANDOVER</p>', unsafe_allow_html=True)
            if st.button(f"📦 All Handover ({len(handover):,})", key="sb_handover", use_container_width=True):
                st.session_state.page = 'handover'
                st.rerun()
            
            st.markdown('<p style="color:#22C55E;font-size:0.75rem;font-weight:700;margin:20px 0 10px 0;">📍 PK ZONE</p>', unsafe_allow_html=True)
            if st.button(f"📋 Normal ({len(pk_normal):,})", key="sb_pk_normal", use_container_width=True):
                st.session_state.page = 'pk_normal'
                st.rerun()
            if st.button(f"🤖 AI ({len(pk_ai):,})", key="sb_pk_ai", use_container_width=True):
                st.session_state.page = 'pk_ai'
                st.rerun()
            
            st.markdown('<p style="color:#22C55E;font-size:0.75rem;font-weight:700;margin:20px 0 10px 0;">🏢 QC CENTER</p>', unsafe_allow_html=True)
            if st.button(f"📋 Normal ({len(qc_normal):,})", key="sb_qc_normal", use_container_width=True):
                st.session_state.page = 'qc_normal'
                st.rerun()
            if st.button(f"🤖 AI ({len(qc_ai):,})", key="sb_qc_ai", use_container_width=True):
                st.session_state.page = 'qc_ai'
                st.rerun()
            
            st.markdown('<p style="color:#60A5FA;font-size:0.75rem;font-weight:700;margin:20px 0 10px 0;">📊 AGING</p>', unsafe_allow_html=True)
            
            pk_aging_data = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            pk_aging_options = ["PK Zone Aging..."] + [f"{b} ({pk_aging_data.get(b, 0)})" for b in BUCKET_ORDER if pk_aging_data.get(b, 0) > 0]
            selected_pk = st.selectbox("PK", pk_aging_options, key="sb_pk_aging_dd", label_visibility="collapsed")
            if selected_pk != "PK Zone Aging...":
                bucket = selected_pk.split(" (")[0]
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = 'PK Zone'
                st.session_state.aging_bucket = bucket
                st.rerun()
            
            qc_aging_data = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            qc_aging_options = ["QC Center Aging..."] + [f"{b} ({qc_aging_data.get(b, 0)})" for b in BUCKET_ORDER if qc_aging_data.get(b, 0) > 0]
            selected_qc = st.selectbox("QC", qc_aging_options, key="sb_qc_aging_dd", label_visibility="collapsed")
            if selected_qc != "QC Center Aging...":
                bucket = selected_qc.split(" (")[0]
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = 'PK QC Center'
                st.session_state.aging_bucket = bucket
                st.rerun()
            
            ho_aging_data = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            ho_aging_options = ["Handover Aging..."] + [f"{b} ({ho_aging_data.get(b, 0)})" for b in BUCKET_ORDER if ho_aging_data.get(b, 0) > 0]
            selected_ho = st.selectbox("HO", ho_aging_options, key="sb_ho_aging_dd", label_visibility="collapsed")
            if selected_ho != "Handover Aging...":
                bucket = selected_ho.split(" (")[0]
                st.session_state.page = 'handover_aging_detail'
                st.session_state.handover_bucket = bucket
                st.rerun()

    # ==================== MAIN CONTENT ====================
    with main_col:
        
        if not st.session_state.show_sidebar:
            if st.button("☰ Sidebar", key="open_btn"):
                st.session_state.show_sidebar = True
                st.rerun()

        # ==================== HOME PAGE ====================
        if st.session_state.page == 'home':
            
            st.markdown("""
                <div class="main-header-container">
                    <div class="main-header-title">
                        <span class="main-header-icon">⚡</span>
                        <span class="main-header-text">G-Ops Backlog Dashboard</span>
                    </div>
                    <p class="main-header-subtitle">📊 Real-time Operations Monitoring | Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
                </div>
            """, unsafe_allow_html=True)
            
            # ==================== SEARCH BOX ====================
            st.markdown('<div class="search-container">', unsafe_allow_html=True)
            
            search_col1, search_col2 = st.columns([4, 1])
            with search_col1:
                search_query = st.text_input(
                    "🔍 Quick Search",
                    placeholder="Enter Order Number or Vendor Name...",
                    key="main_search",
                    label_visibility="collapsed"
                )
            with search_col2:
                search_btn = st.button("🔍 Search", key="search_btn", use_container_width=True)
            
            if search_query and len(search_query) >= 3:
                search_term = search_query.strip().lower()
                
                order_matches = all_data[all_data['order_number'].astype(str).str.lower().str.contains(search_term, na=False)]
                vendor_matches = all_data[all_data['vendor'].astype(str).str.lower().str.contains(search_term, na=False)]
                unique_vendors = vendor_matches['vendor'].dropna().unique()
                
                if len(order_matches) > 0:
                    st.markdown(f"<p style='color:#22C55E;font-weight:700;margin-top:15px;'>✅ Found {len(order_matches)} order(s)</p>", unsafe_allow_html=True)
                    
                    for idx, (_, order) in enumerate(order_matches.head(5).iterrows()):
                        with st.expander(f"📦 Order: {order.get('order_number', 'N/A')}", expanded=(idx==0)):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Order Number:** {order.get('order_number', 'N/A')}")
                                st.markdown(f"**Fleek ID:** {order.get('fleek_id', 'N/A')}")
                                st.markdown(f"**Customer:** {order.get('customer_name', 'N/A')}")
                                st.markdown(f"**Country:** {order.get('customer_country', 'N/A')}")
                                st.markdown(f"**Status:** {order.get('latest_status', 'N/A')}")
                            with col2:
                                st.markdown(f"**Vendor:** {order.get('vendor', 'N/A')}")
                                st.markdown(f"**Item:** {order.get('item_name', 'N/A')[:50]}...")
                                st.markdown(f"**Amount:** ${order.get('total_order_line_amount', 'N/A')}")
                                st.markdown(f"**Brand:** {order.get('product_brand', 'N/A')}")
                                st.markdown(f"**Aging:** {order.get('aging_days', 'N/A')} days ({order.get('aging_bucket', 'N/A')})")
                    
                    if len(order_matches) > 5:
                        st.info(f"Showing first 5 of {len(order_matches)} orders. Be more specific to narrow results.")
                
                if len(unique_vendors) > 0 and len(order_matches) == 0:
                    st.markdown(f"<p style='color:#A78BFA;font-weight:700;margin-top:15px;'>🏪 Found {len(unique_vendors)} vendor(s)</p>", unsafe_allow_html=True)
                    
                    for vendor in unique_vendors[:10]:
                        vendor_order_count = len(vendor_matches[vendor_matches['vendor'] == vendor])
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"""
                                <div class="vendor-match-card">
                                    <span class="vendor-match-name">{vendor}</span><br>
                                    <span class="vendor-match-count">{vendor_order_count} orders in backlog</span>
                                </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            if st.button(f"View", key=f"view_vendor_{vendor[:20]}", use_container_width=True):
                                st.session_state.page = 'search_vendor_orders'
                                st.session_state.search_result_vendor = vendor
                                st.rerun()
                
                if len(order_matches) == 0 and len(unique_vendors) == 0:
                    st.warning(f"❌ No orders or vendors found for '{search_query}'")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
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
            
            col1, col2, col3 = st.columns(3)
            
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
            
            st.markdown('<div class="section-header-white">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
            
            pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            
            col1, col2, col3 = st.columns(3)
            
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
            
            st.markdown('<div class="section-header-white">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
            
            pk_vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
            pk_vendor_counts.columns = ['Vendor', 'Orders']
            
            h1, h2, h3 = st.columns([5, 1, 2])
            with h1:
                st.markdown("<span class='vendor-header'>Vendor Name</span>", unsafe_allow_html=True)
            with h2:
                st.markdown("<span class='vendor-header'>Qty</span>", unsafe_allow_html=True)
            with h3:
                st.markdown("<span class='vendor-header'>Comment</span>", unsafe_allow_html=True)
            
            for i, (_, row) in enumerate(pk_vendor_counts.iterrows()):
                vendor_key = f"pk_{row['Vendor']}"
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
            
            st.markdown(f"<p style='color:#888888;font-size:0.9rem;margin-top:20px;'>{len(pk_vendor_counts)} vendors | {len(pk_normal):,} total orders</p>", unsafe_allow_html=True)

        # ==================== 3PL WEEKLY SUMMARY PAGE ====================
        elif st.session_state.page == '3pl_summary':
            
            if st.button("← Back to Dashboard", key="back_3pl"):
                st.session_state.page = 'home'
                st.rerun()
            
            st.markdown("""
                <div class="main-header-container" style="margin-top:15px;">
                    <div class="main-header-title">
                        <span class="main-header-icon">🚀</span>
                        <span class="main-header-text" style="font-size:36px;">3PL Weekly Summary</span>
                    </div>
                    <p class="main-header-subtitle">📦 Logistics Partner Performance | Weekly Aggregated View</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # --- Week selector: default = current week's Monday ---
            today = datetime.now().date()
            days_since_monday = today.weekday()  # Monday=0, Sunday=6
            default_monday = today - timedelta(days=days_since_monday)
            
            dc1, dc2 = st.columns([2, 4])
            with dc1:
                selected_monday = st.date_input(
                    "📅 Week Start (Monday)",
                    value=default_monday,
                    key="tpl_week_start"
                )
            
            # Build 7 days Mon-Sun
            week_days = [selected_monday + timedelta(days=i) for i in range(7)]
            day_labels = [d.strftime("%a %d %b") for d in week_days]
            day_strs   = [d.strftime("%Y-%m-%d") for d in week_days]
            
            st.markdown(f"<p style='color:#666;font-size:0.85rem;margin-bottom:20px;'>Showing week: <strong style='color:#a78bfa;'>{week_days[0].strftime('%d %b %Y')}</strong> → <strong style='color:#a78bfa;'>{week_days[6].strftime('%d %b %Y')}</strong></p>", unsafe_allow_html=True)
            
            # --- Load all needed sheets once (raw, no header) ---
            with st.spinner("Loading 3PL data from Google Sheets..."):
                sheet_cache = {}
                for sheet_name in TPL_SHEETS_NEEDED:
                    sheet_cache[sheet_name] = load_3pl_sheet(sheet_name)
            
            # ⚠️ Note: sheet_cache values are raw DataFrames with no header row (header=None)
            # Row indices are 0-based. Col A = index 0, Col B = index 1, etc.
            
            # --- Helper: get TOTAL SUMMARY row for a provider section ---
            def get_provider_total_row(sheet_df, provider_label):
                """
                Sheet has multiple provider sections stacked vertically.
                Each section starts with a header row containing provider name in col A (col index 0).
                TOTAL SUMMARY row comes after region rows within that section.
                We find the section start, then find the NEXT TOTAL SUMMARY row after it.
                """
                if sheet_df.empty or len(sheet_df.columns) < 5:
                    return None
                
                cfg = TPL_PROVIDER_CONFIG[provider_label]
                section_marker = cfg["section_marker"].upper().strip()
                
                col_a = sheet_df.iloc[:, 0].astype(str).str.upper().str.strip()
                
                # Find section header row
                section_start = None
                for i, val in enumerate(col_a):
                    if section_marker in val:
                        section_start = i
                        break
                
                if section_start is None:
                    # Try partial match
                    # Extract key words from marker
                    key_words = section_marker.replace('(', '').replace(')', '').split()
                    for i, val in enumerate(col_a):
                        if all(w in val for w in key_words):
                            section_start = i
                            break
                
                if section_start is None:
                    return None
                
                # Find TOTAL SUMMARY row after section_start
                for i in range(section_start + 1, min(section_start + 30, len(sheet_df))):
                    val = str(sheet_df.iloc[i, 0]).upper().strip()
                    if 'TOTAL' in val and 'SUMMARY' in val:
                        return sheet_df.iloc[i]
                    # Also accept just TOTAL
                    if val.startswith('TOTAL'):
                        return sheet_df.iloc[i]
                
                return None
            
            # --- Get metrics for a provider for a specific day index (0=Mon, 6=Sun) ---
            def get_provider_day_metrics(sheet_df, provider_label, day_index):
                """
                day_index: 0=Monday, 1=Tuesday, ..., 6=Sunday
                Each day has 5 columns: Orders, Boxes, Weight, <20kg, 20kg+
                Starting at day_col_start (col index 1 = B)
                So Monday = cols 1,2,3,4,5 | Tuesday = cols 6,7,8,9,10 | etc.
                """
                total_row = get_provider_total_row(sheet_df, provider_label)
                
                if total_row is None:
                    return {"Orders": 0, "Boxes": 0, "Weight": 0.0, "<20kg": 0, "20kg+": 0}
                
                cfg = TPL_PROVIDER_CONFIG[provider_label]
                base = cfg["day_col_start"]  # e.g. 1 for col B
                
                # Column offsets within each day block: Orders=0, Boxes=1, Weight=2, <20kg=3, 20kg+=4
                day_base = base + (day_index * 5)
                
                def safe_val(col_idx, is_float=False):
                    try:
                        if col_idx >= len(total_row):
                            return 0
                        v = total_row.iloc[col_idx]
                        if pd.isna(v) or str(v).strip() in ['', '-', '—', 'nan']:
                            return 0
                        return round(float(str(v).replace(',', '')), 1) if is_float else int(float(str(v).replace(',', '')))
                    except:
                        return 0
                
                return {
                    "Orders": safe_val(day_base + 0),
                    "Boxes":  safe_val(day_base + 1),
                    "Weight": safe_val(day_base + 2, is_float=True),
                    "<20kg":  safe_val(day_base + 3),
                    "20kg+":  safe_val(day_base + 4),
                }
            
            # --- Build table data ---
            providers_list = list(TPL_PROVIDER_CONFIG.keys())
            metrics_keys = ["Orders", "Boxes", "Weight", "<20kg", "20kg+"]
            
            # table_data[provider][day_index] = {Orders, Boxes, Weight, <20kg, 20kg+}
            table_data = {}
            for prov in providers_list:
                sheet_name = TPL_PROVIDER_CONFIG[prov]["sheet"]
                sheet_df   = sheet_cache.get(sheet_name, pd.DataFrame())
                table_data[prov] = {}
                for day_idx in range(7):
                    table_data[prov][day_idx] = get_provider_day_metrics(sheet_df, prov, day_idx)
            
            # --- Build HTML table ---
            metric_short = {"Orders": "Ord", "Boxes": "Box", "Weight": "Wt", "<20kg": "<20", "20kg+": "20+"}
            
            html = '<div class="tpl-table-wrapper"><table class="tpl-table">'
            
            # Row 1: day group headers
            html += '<thead><tr>'
            html += '<th class="provider-header" rowspan="2">Provider</th>'
            for dl in day_labels:
                html += f'<th class="day-group" colspan="5">{dl}</th>'
            html += '<th class="day-group" colspan="5">📊 TOTAL</th>'
            html += '</tr>'
            
            # Row 2: metric sub-headers
            html += '<tr>'
            total_cols = len(day_labels) + 1  # 7 days + 1 total
            for _ in range(total_cols):
                for mk in metrics_keys:
                    html += f'<th>{metric_short[mk]}</th>'
            html += '</tr></thead>'
            
            # Body rows
            html += '<tbody>'
            
            # Grand totals across all providers
            grand_day_totals = {day_idx: {mk: 0 for mk in metrics_keys} for day_idx in range(7)}
            grand_week_total = {mk: 0 for mk in metrics_keys}
            
            for prov in providers_list:
                html += '<tr>'
                html += f'<td class="provider-name">{prov}</td>'
                
                prov_week_total = {mk: 0 for mk in metrics_keys}
                
                for day_idx in range(7):
                    day_m = table_data[prov][day_idx]
                    for mk in metrics_keys:
                        val = day_m[mk]
                        prov_week_total[mk] += val
                        grand_day_totals[day_idx][mk] += val
                        
                        if val == 0:
                            html += f'<td class="tpl-zero">—</td>'
                        else:
                            disp = f"{val:,.1f}" if mk == "Weight" else f"{val:,}"
                            html += f'<td class="tpl-value-highlight">{disp}</td>'
                
                # Provider week total
                for mk in metrics_keys:
                    val = prov_week_total[mk]
                    grand_week_total[mk] += val
                    if val == 0:
                        html += f'<td class="tpl-zero">—</td>'
                    else:
                        disp = f"{val:,.1f}" if mk == "Weight" else f"{val:,}"
                        html += f'<td class="tpl-value-highlight">{disp}</td>'
                
                html += '</tr>'
            
            # Grand total row
            html += '<tr class="total-row">'
            html += '<td class="provider-name">🏆 GRAND TOTAL</td>'
            for day_idx in range(7):
                for mk in metrics_keys:
                    val = grand_day_totals[day_idx][mk]
                    if val == 0:
                        html += f'<td class="tpl-zero">—</td>'
                    else:
                        disp = f"{val:,.1f}" if mk == "Weight" else f"{val:,}"
                        html += f'<td>{disp}</td>'
            for mk in metrics_keys:
                val = grand_week_total[mk]
                if val == 0:
                    html += f'<td class="tpl-zero">—</td>'
                else:
                    disp = f"{val:,.1f}" if mk == "Weight" else f"{val:,}"
                    html += f'<td>{disp}</td>'
            html += '</tr>'
            
            html += '</tbody></table></div>'
            
            # Legend
            html += """
            <div style="margin-top:15px;padding:12px 18px;background:#111;border-radius:10px;border:1px solid #222;">
                <span style="color:#666;font-size:0.78rem;font-weight:600;">
                📌 Column Key: &nbsp;
                <span style="color:#a78bfa;">Ord</span> = Orders &nbsp;|&nbsp;
                <span style="color:#a78bfa;">Box</span> = Boxes &nbsp;|&nbsp;
                <span style="color:#a78bfa;">Wt</span> = Weight (kg) &nbsp;|&nbsp;
                <span style="color:#a78bfa;">&lt;20</span> = Below 20kg &nbsp;|&nbsp;
                <span style="color:#a78bfa;">20+</span> = 20kg &amp; above &nbsp;|&nbsp;
                <span style="color:#3a3a3a;">—</span> = No data / Zero
                </span>
            </div>
            """
            
            st.markdown(html, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#444;font-size:0.78rem;text-align:center;'>Data refreshes every 5 minutes · 3PL Sheet ID: {TPL_SHEET_ID}</p>", unsafe_allow_html=True)

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
            elif page == 'search_vendor_orders':
                vendor = st.session_state.search_result_vendor
                title = f"🏪 {vendor[:40]}"
                data_view = all_data[all_data['vendor'] == vendor]
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
    import traceback
    st.code(traceback.format_exc())
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
