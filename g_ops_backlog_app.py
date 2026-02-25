import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import urllib.parse

# Page config
st.set_page_config(page_title="Command Center", page_icon="⚡", layout="wide")

# ==========================================
# SESSION STATE INITIALIZATION (100% Restored)
# ==========================================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'show_sidebar' not in st.session_state: st.session_state.show_sidebar = True
if 'aging_zone' not in st.session_state: st.session_state.aging_zone = None
if 'aging_bucket' not in st.session_state: st.session_state.aging_bucket = None
if 'vendor_name' not in st.session_state: st.session_state.vendor_name = None
if 'vendor_zone' not in st.session_state: st.session_state.vendor_zone = None
if 'handover_bucket' not in st.session_state: st.session_state.handover_bucket = None
if 'vendor_comments' not in st.session_state: st.session_state.vendor_comments = {}
if 'search_result_order' not in st.session_state: st.session_state.search_result_order = None
if 'search_result_vendor' not in st.session_state: st.session_state.search_result_vendor = None

# ==========================================
# ULTIMATE MODERN SAAS CSS (Light Theme)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp { background-color: #F8FAFC !important; }
header {visibility: hidden;} #MainMenu {visibility: hidden;} footer {visibility: hidden;}

/* SIDEBAR STYLING */
div[data-testid="column"]:nth-of-type(1) { background-color: #0F172A; padding: 20px 10px 100vh 10px !important; margin-top: -80px; border-right: 1px solid #1E293B; }
div[data-testid="column"]:nth-of-type(1) .stButton > button { background-color: transparent !important; color: #94A3B8 !important; border: none !important; text-align: left !important; justify-content: flex-start !important; font-weight: 600 !important; font-size: 13px !important; padding: 10px 16px !important; border-radius: 8px !important; box-shadow: none !important; transition: all 0.2s ease; margin-bottom: 2px;}
div[data-testid="column"]:nth-of-type(1) .stButton > button:hover { background-color: #1E293B !important; color: #F8FAFC !important; }
.sb-header { color: #64748B; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin: 20px 0 10px 15px; }
.stSelectbox > div > div { background: #1E293B !important; border: 1px solid #334155 !important; border-radius: 8px !important; color: #E2E8F0 !important; font-size: 13px !important; min-height: 36px !important; }

/* MAIN CONTENT AREA */
div[data-testid="column"]:nth-of-type(2) { padding: 20px 40px !important; margin-top: -60px; }
.top-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #E2E8F0; padding-bottom: 15px; }
.top-header-title { font-size: 24px; font-weight: 800; color: #0F172A; }
.top-header-user { display: flex; align-items: center; background: #FFFFFF; padding: 6px 14px; border-radius: 20px; border: 1px solid #E2E8F0; font-size: 13px; font-weight: 600; color: #475569; }
.page-main-title { font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 5px; }
.page-sub-title { font-size: 14px; color: #64748B; font-weight: 500; margin-bottom: 25px; }
.section-header-saas { font-size: 1.1rem; font-weight: 800; color: #0F172A; margin: 30px 0 15px 0; padding-bottom: 10px; border-bottom: 2px solid #E2E8F0; }

/* MODERN METRIC CARDS */
.saas-card { background: #FFFFFF; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); border: 1px solid #E2E8F0; position: relative; overflow: hidden; transition: transform 0.2s ease;}
.saas-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.card-blue { border-top: 4px solid #4F46E5; }
.card-orange { border-top: 4px solid #F59E0B; }
.card-purple { border-top: 4px solid #8B5CF6; }
.card-green { border-top: 4px solid #10B981; }
.saas-card .c-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;}
.saas-card .c-value { font-size: 32px; font-weight: 800; color: #0F172A; line-height: 1;}

/* INNER INFO CARDS */
.info-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 15px; text-align: center; }
.info-card .i-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 5px; }
.info-card .i-value { font-size: 24px; font-weight: 800; color: #4F46E5; }

/* SEARCH BAR & INPUTS */
.search-box-container { background: #FFFFFF; border-radius: 16px; padding: 20px; text-align: center; border: 1px solid #E2E8F0; margin-bottom: 30px; }
.stTextInput > div > div > input { background-color: #F8FAFC !important; border: 1px solid #E2E8F0 !important; border-radius: 8px !important; color: #0F172A !important; font-size: 14px !important; }
.stTextInput > div > div > input:focus { border-color: #4F46E5 !important; box-shadow: 0 0 0 2px rgba(79,70,229,0.2) !important; }

/* BUTTONS */
div[data-testid="column"]:nth-of-type(2) .stButton > button { background-color: #F1F5F9 !important; color: #475569 !important; border: 1px solid #E2E8F0 !important; border-radius: 6px !important; font-weight: 600 !important; box-shadow: none !important; transition: all 0.2s; font-size: 12px !important; min-height: 32px !important;}
div[data-testid="column"]:nth-of-type(2) .stButton > button:hover { background-color: #E2E8F0 !important; color: #0F172A !important; }
button[kind="primary"] { background-color: #4F46E5 !important; color: #FFFFFF !important; border: none !important; }
button[kind="primary"]:hover { background-color: #4338CA !important; }

/* AGING & VENDORS */
.aging-bucket-text { color: #475569; font-size: 13px; font-weight: 600; }
.vendor-name-text { color: #0F172A; font-size: 13px; font-weight: 600; }
.vendor-header { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; }

/* 3PL VIP TABLE (SAAS MODE) */
.vip-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; background: #FFFFFF; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #E2E8F0; }
.vip-table th { background-color: #F8FAFC; color: #475569; padding: 12px; text-align: center; font-size: 11px; font-weight: 700; border-bottom: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; text-transform: uppercase; }
.vip-table td { padding: 12px 10px; text-align: center; border-bottom: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; font-size: 12px; color: #334155; font-weight: 500;}
.vip-table .region-col { font-weight: 700; text-align: left; background-color: #FFFFFF; color: #0F172A; }
.vip-table .day-header { background-color: #EEF2FF; color: #4F46E5; font-size: 12px; }
.vip-table .sub-header { background-color: #FFFFFF; color: #64748B; font-size: 10px; }
.vip-table tr:hover td { background-color: #F8FAFC; }
.vip-table .total-row td { background-color: #F0FDF4 !important; color: #059669 !important; font-weight: 800; font-size: 13px; border-top: 2px solid #D1FAE5; }
.vip-provider-title { background: #FFFFFF; color: #0F172A; padding: 15px 20px; font-size: 16px; font-weight: 800; border-top-left-radius: 12px; border-top-right-radius: 12px; margin-top: 20px; border: 1px solid #E2E8F0; border-bottom: none; display: flex; align-items: center; gap: 10px;}
.vip-provider-title::before { content: ''; display: inline-block; width: 4px; height: 16px; background-color: #4F46E5; border-radius: 2px; }

[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #E2E8F0; }
h1, h2, h3, h4, h5, p, span, div { color: #334155; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING (SEPARATED IDs - SAFE MODE)
# ==========================================
SHEET_ID_GOPS = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o" 
SHEET_ID_3PL = "1V03fqI2tGbY3ImkQaoZGwJ98iyrN4z_GXRKRP023zUY"

@st.cache_data(ttl=600, show_spinner=False)
def load_ai_fleek_ids():
    ai_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_GOPS}/gviz/tq?tqx=out:csv&sheet=AI"
    try:
        ai_df = pd.read_csv(ai_url, low_memory=False)
        return set(ai_df['fleek_id'].astype(str).str.strip().tolist())
    except: return set()

@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_GOPS}/gviz/tq?tqx=out:csv&sheet=Extract%201"
    df = pd.read_csv(url, low_memory=False)
    ai_fleek_ids = load_ai_fleek_ids()
    def get_qc_zone(row):
        is_zone = str(row.get('is_zone_vendor', '')).strip().upper()
        vc = str(row.get('vendor_country', '')).strip().upper()
        if vc == 'PK': return 'PK Zone' if is_zone == 'TRUE' else 'PK QC Center'
        elif vc == 'IN': return 'IN Zone' if is_zone == 'TRUE' else 'IN QC Center'
        return 'Other'
    df['QC or zone'] = df.apply(get_qc_zone, axis=1)
    df['Order Type'] = df['fleek_id'].apply(lambda x: 'AI Order' if str(x).strip() in ai_fleek_ids else 'Normal Order')
    return df

@st.cache_data(ttl=600, show_spinner=False)
def process_data(df):
    now = datetime.now()
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))].copy()
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == '': return pd.NaT
        date_str = str(date_str).strip()
        for fmt in ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y', '%B %d, %Y, %H:%M', '%Y-%m-%d %H:%M:%S']:
            try: return pd.to_datetime(date_str, format=fmt)
            except: continue
        try: return pd.to_datetime(date_str, dayfirst=True)
        except: return pd.NaT
    approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
    approved['aging_days'] = (now - approved['qc_date']).dt.days
    handover['handover_date'] = handover['logistics_partner_handedover_at'].apply(parse_date)
    handover['aging_days'] = (now - handover['handover_date']).dt.days
    def assign_buckets(days_series):
        conditions = [ days_series == 0, days_series == 1, days_series == 2, days_series == 3, days_series == 4, days_series == 5, (days_series >= 6) & (days_series <= 7), (days_series >= 8) & (days_series <= 10), (days_series >= 11) & (days_series <= 15), (days_series >= 16) & (days_series <= 20), (days_series >= 21) & (days_series <= 25), (days_series >= 26) & (days_series <= 30), days_series > 30 ]
        choices = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', '6-7 days', '8-10 days', '11-15 days', '16-20 days', '21-25 days', '26-30 days', '30+ days']
        return np.select(conditions, choices, default=None)
    approved['aging_bucket'] = assign_buckets(approved['aging_days'])
    handover['aging_bucket'] = assign_buckets(handover['aging_days'])
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    return {'approved': approved, 'handover': handover, 'pk_zone': pk_zone, 'qc_center': qc_center, 'pk_normal': pk_zone[pk_zone['Order Type'] == 'Normal Order'], 'pk_ai': pk_zone[pk_zone['Order Type'] == 'AI Order'], 'qc_normal': qc_center[qc_center['Order Type'] == 'Normal Order'], 'qc_ai': qc_center[qc_center['Order Type'] == 'AI Order'], 'all_data': pd.concat([approved, handover], ignore_index=True)}

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', '6-7 days', '8-10 days', '11-15 days', '16-20 days', '21-25 days', '26-30 days', '30+ days']
VENDOR_ACTION_OPTIONS = ['--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']
DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 'vendor', 'item_name', 'total_order_line_amount', 'product_brand', 'logistics_partner_name', 'aging_days', 'aging_bucket']

# ==========================================
# 3PL SUMMARY HTML GENERATOR
# ==========================================
@st.cache_data(ttl=600, show_spinner=False)
def load_3pl_sheet(sheet_name):
    try:
        sheet_encoded = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_3PL}/gviz/tq?tqx=out:csv&sheet={sheet_encoded}"
        return pd.read_csv(url, low_memory=False)
    except Exception as e: return pd.DataFrame()

def generate_3pl_html(start_date):
    configs = [
        {"title": "GLOBAL EXPRESS (QC CENTER)", "sh": "GE QC Center & Zone", "rCol": 7, "dCol": 1, "bCol": 2, "wCol": 5},
        {"title": "GLOBAL EXPRESS (ZONES)", "sh": "GE QC Center & Zone", "rCol": 16, "dCol": 10, "bCol": 11, "wCol": 15},
        {"title": "ECL LOGISTICS (QC CENTER)", "sh": "ECL QC Center & Zone", "rCol": 7, "dCol": 1, "bCol": 2, "wCol": 5},
        {"title": "ECL LOGISTICS (ZONES)", "sh": "ECL QC Center & Zone", "rCol": 16, "dCol": 10, "bCol": 11, "wCol": 14},
        {"title": "KERRY LOGISTICS", "sh": "Kerry", "rCol": 6, "dCol": 1, "bCol": 2, "wCol": 5},
        {"title": "APX EXPRESS", "sh": "APX", "rCol": 7, "dCol": 1, "bCol": 2, "wCol": 5}
    ]
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    dates = [pd.to_datetime(start_date) + timedelta(days=i) for i in range(7)]
    html = ""
    for cfg in configs:
        df = load_3pl_sheet(cfg["sh"])
        if df.empty: continue
        try:
            max_col = max(cfg['rCol'], cfg['dCol'], cfg['bCol'], cfg['wCol'])
            if len(df.columns) <= max_col: continue
            df_slice = df.iloc[:, [cfg['dCol'], cfg['rCol'], cfg['bCol'], cfg['wCol']]].copy()
            df_slice.columns = ['Date', 'Region', 'Boxes', 'Weight']
            df_slice['Date'] = pd.to_datetime(df_slice['Date'], format='mixed', dayfirst=True, errors='coerce')
            df_slice['Boxes'] = pd.to_numeric(df_slice['Boxes'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            df_slice['Weight'] = pd.to_numeric(df_slice['Weight'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            week_mask = (df_slice['Date'] >= dates[0]) & (df_slice['Date'] <= dates[-1])
            valid_region = df_slice['Region'].notna() & (df_slice['Region'].astype(str).str.strip() != '') & (df_slice['Region'] != 'Country')
            filtered_df = df_slice[week_mask & valid_region]
            regions = sorted(filtered_df['Region'].unique().tolist())
            if not regions: continue
            
            html += f'<div class="vip-provider-title">{cfg["title"]}</div><table class="vip-table">'
            html += '<tr><th rowspan="2" class="region-col">ACTIVE REGIONS</th>'
            for d in days: html += f'<th colspan="5" class="day-header">{d}</th>'
            html += '</tr><tr>'
            for _ in days: html += '<th class="sub-header">Orders</th><th class="sub-header">Boxes</th><th class="sub-header">Weight</th><th class="sub-header"><20kg</th><th class="sub-header">20kg+</th>'
            html += '</tr>'
            totals = [0] * 35 
            for r in regions:
                html += f'<tr><td class="region-col">{r}</td>'
                reg_df = filtered_df[filtered_df['Region'] == r]
                for i, d in enumerate(dates):
                    day_df = reg_df[reg_df['Date'] == d]
                    orders = len(day_df)
                    boxes = day_df['Boxes'].sum()
                    weight = day_df['Weight'].sum()
                    lt_20 = len(day_df[day_df['Weight'] < 20])
                    gt_20 = len(day_df[day_df['Weight'] >= 20])
                    vals = [orders, boxes, weight, lt_20, gt_20]
                    for j, val in enumerate(vals):
                        totals[(i*5)+j] += val
                        disp_val = f"{val:,.0f}" if j != 2 else f"{val:,.2f}"
                        html += f'<td>{disp_val if val > 0 else "-"}</td>'
                html += '</tr>'
            html += '<tr class="total-row"><td>TOTAL SUMMARY</td>'
            for idx, val in enumerate(totals):
                disp_val = f"{val:,.0f}" if (idx % 5) != 2 else f"{val:,.2f}"
                html += f'<td>{disp_val if val > 0 else "-"}</td>'
            html += '</tr></table>'
        except Exception as e: continue
    return html

# ==========================================
# MAIN APP LAYOUT
# ==========================================
try:
    with st.spinner('Syncing Real-time Data...'):
        df = load_data()
        data = process_data(df)
    
    approved, handover, pk_zone, qc_center = data['approved'], data['handover'], data['pk_zone'], data['qc_center']
    pk_normal, pk_ai, qc_normal, qc_ai = data['pk_normal'], data['pk_ai'], data['qc_normal'], data['qc_ai']
    all_data = data['all_data']

    if st.session_state.show_sidebar: sidebar_col, main_col = st.columns([1, 4.5])
    else: sidebar_col, main_col = None, st.container()

    # --- FULL SIDEBAR RESTORED (With Aging Dropdowns) ---
    if st.session_state.show_sidebar and sidebar_col:
        with sidebar_col:
            st.markdown("""
                <div style="padding: 10px 0 30px 0; display: flex; align-items: center; gap: 12px;">
                    <div style="background: #4F46E5; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px;">📦</div>
                    <span style="color: #FFFFFF; font-size: 18px; font-weight: 800; letter-spacing: 0.5px;">G-OPS</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="sb-header">MAIN MENU</div>', unsafe_allow_html=True)
            if st.button("📊 Dashboard Overview", use_container_width=True): st.session_state.page = 'home'; st.rerun()
            if st.button(f"🚚 Manage Handover ({len(handover):,})", use_container_width=True): st.session_state.page = 'handover'; st.rerun()
            
            st.markdown('<div class="sb-header">EXECUTIVE VIEWS</div>', unsafe_allow_html=True)
            if st.button("📈 3PL Summary", use_container_width=True): st.session_state.page = '3pl_summary'; st.rerun()
            
            st.markdown('<div class="sb-header">OPERATIONS</div>', unsafe_allow_html=True)
            if st.button(f"📍 PK Zone Normal ({len(pk_normal):,})", use_container_width=True): st.session_state.page = 'pk_normal'; st.rerun()
            if st.button(f"🤖 PK Zone AI ({len(pk_ai):,})", use_container_width=True): st.session_state.page = 'pk_ai'; st.rerun()
            if st.button(f"🏢 QC Normal ({len(qc_normal):,})", use_container_width=True): st.session_state.page = 'qc_normal'; st.rerun()
            if st.button(f"🤖 QC AI ({len(qc_ai):,})", use_container_width=True): st.session_state.page = 'qc_ai'; st.rerun()

            # AGING DROPDOWNS (Restored)
            st.markdown('<div class="sb-header">AGING ANALYSIS</div>', unsafe_allow_html=True)
            pk_aging_data = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            pk_aging_options = ["📍 PK Zone Aging..."] + [f"{b} ({pk_aging_data.get(b, 0)})" for b in BUCKET_ORDER if pk_aging_data.get(b, 0) > 0]
            selected_pk = st.selectbox("PK", pk_aging_options, key="sb_pk_aging_dd", label_visibility="collapsed")
            if selected_pk != "📍 PK Zone Aging...":
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = 'PK Zone'
                st.session_state.aging_bucket = selected_pk.split(" (")[0]
                st.rerun()
            
            qc_aging_data = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            qc_aging_options = ["🏢 QC Center Aging..."] + [f"{b} ({qc_aging_data.get(b, 0)})" for b in BUCKET_ORDER if qc_aging_data.get(b, 0) > 0]
            selected_qc = st.selectbox("QC", qc_aging_options, key="sb_qc_aging_dd", label_visibility="collapsed")
            if selected_qc != "🏢 QC Center Aging...":
                st.session_state.page = 'aging_detail'
                st.session_state.aging_zone = 'PK QC Center'
                st.session_state.aging_bucket = selected_qc.split(" (")[0]
                st.rerun()
            
            ho_aging_data = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            ho_aging_options = ["🚚 Handover Aging..."] + [f"{b} ({ho_aging_data.get(b, 0)})" for b in BUCKET_ORDER if ho_aging_data.get(b, 0) > 0]
            selected_ho = st.selectbox("HO", ho_aging_options, key="sb_ho_aging_dd", label_visibility="collapsed")
            if selected_ho != "🚚 Handover Aging...":
                st.session_state.page = 'handover_aging_detail'
                st.session_state.handover_bucket = selected_ho.split(" (")[0]
                st.rerun()

    # --- MAIN CONTENT AREA ---
    with main_col:
        st.markdown(f"""
            <div class="top-header-row">
                <div class="top-header-title">Command Center</div>
                <div class="top-header-user">👤 Admin Workspace</div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.show_sidebar:
            if st.button("☰ Show Menu"): st.session_state.show_sidebar = True; st.rerun()

        # ---------------------------------------------------------
        # PAGE: HOME (100% RESTORED - AGING & VENDORS ARE BACK!)
        # ---------------------------------------------------------
        if st.session_state.page == 'home':
            st.markdown('<div class="page-main-title">Overview</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="page-sub-title">Real-time warehouse operations status. Last sync: {datetime.now().strftime("%I:%M %p")}</div>', unsafe_allow_html=True)
            
            # 1. MAIN METRIC CARDS
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(f'''<div class="saas-card card-blue"><div class="c-label">Total Approved</div><div class="c-value">{len(approved):,}</div><div class="c-icon">📋</div></div>''', unsafe_allow_html=True)
            with m2: st.markdown(f'''<div class="saas-card card-orange"><div class="c-label">PK Zone</div><div class="c-value">{len(pk_zone):,}</div><div class="c-icon">📍</div></div>''', unsafe_allow_html=True)
            with m3: st.markdown(f'''<div class="saas-card card-purple"><div class="c-label">QC Center</div><div class="c-value">{len(qc_center):,}</div><div class="c-icon">🏢</div></div>''', unsafe_allow_html=True)
            with m4: st.markdown(f'''<div class="saas-card card-green"><div class="c-label">Pending Handover</div><div class="c-value">{len(handover):,}</div><div class="c-icon">🚚</div></div>''', unsafe_allow_html=True)
            
            # 2. INNER INFO CARDS (Restored from Original)
            st.markdown('<div class="section-header-saas">Breakdown Summary</div>', unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown(f'''<div class="info-card"><div class="i-label">To Logistics Partner</div><div class="i-value">{len(handover):,}</div></div>''', unsafe_allow_html=True)
                if st.button("View Handover", key="v_handover", use_container_width=True): st.session_state.page = 'handover'; st.rerun()
            with b2:
                c1, c2 = st.columns(2)
                with c1: 
                    st.markdown(f'''<div class="info-card"><div class="i-label">PK Normal</div><div class="i-value">{len(pk_normal):,}</div></div>''', unsafe_allow_html=True)
                    if st.button("View PK Normal", key="v_pkn", use_container_width=True): st.session_state.page = 'pk_normal'; st.rerun()
                with c2: 
                    st.markdown(f'''<div class="info-card"><div class="i-label">PK AI</div><div class="i-value">{len(pk_ai):,}</div></div>''', unsafe_allow_html=True)
                    if st.button("View PK AI", key="v_pka", use_container_width=True): st.session_state.page = 'pk_ai'; st.rerun()
            with b3:
                c1, c2 = st.columns(2)
                with c1: 
                    st.markdown(f'''<div class="info-card"><div class="i-label">QC Normal</div><div class="i-value">{len(qc_normal):,}</div></div>''', unsafe_allow_html=True)
                    if st.button("View QC Normal", key="v_qcn", use_container_width=True): st.session_state.page = 'qc_normal'; st.rerun()
                with c2: 
                    st.markdown(f'''<div class="info-card"><div class="i-label">QC AI</div><div class="i-value">{len(qc_ai):,}</div></div>''', unsafe_allow_html=True)
                    if st.button("View QC AI", key="v_qca", use_container_width=True): st.session_state.page = 'qc_ai'; st.rerun()

            # 3. SEARCH BOX
            st.write("")
            st.markdown('<div class="search-box-container"><div class="search-box-title">Search & Track Orders</div><div class="search-box-sub">Scan order ID or enter manually to view details.</div>', unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns([1, 4, 1])
            with sc2:
                s_col, b_col = st.columns([4, 1])
                with s_col: search_query = st.text_input("", placeholder="🔍 Search Order or Vendor...", label_visibility="collapsed")
                with b_col: search_btn = st.button("Search →", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if search_query and len(search_query) >= 3:
                s = search_query.strip().lower()
                order_m = all_data[all_data['order_number'].astype(str).str.lower().str.contains(s, na=False)]
                if len(order_m) > 0:
                    st.success(f"✅ Found {len(order_m)} matching orders")
                    st.dataframe(order_m[DISPLAY_COLS].head(10), use_container_width=True)

            # 4. AGING ANALYSIS (RESTORED!)
            st.markdown('<div class="section-header-saas">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
            pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            
            a1, a2, a3 = st.columns(3)
            with a1:
                st.markdown('**📍 PK ZONE**', unsafe_allow_html=True)
                for bucket in BUCKET_ORDER:
                    count = pk_aging.get(bucket, 0)
                    st.markdown("<div style='border-bottom:1px solid #E2E8F0; margin-bottom:5px;'></div>", unsafe_allow_html=True)
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"{count}", key=f"pk_a_{bucket}", use_container_width=True):
                            if count > 0:
                                st.session_state.page = 'aging_detail'
                                st.session_state.aging_zone = 'PK Zone'
                                st.session_state.aging_bucket = bucket
                                st.rerun()
                st.markdown(f"<p style='color:#0F172A;font-weight:800;font-size:14px;margin-top:10px;'>Total: {len(pk_normal):,}</p>", unsafe_allow_html=True)
            
            with a2:
                st.markdown('**🏢 QC CENTER**', unsafe_allow_html=True)
                for bucket in BUCKET_ORDER:
                    count = qc_aging.get(bucket, 0)
                    st.markdown("<div style='border-bottom:1px solid #E2E8F0; margin-bottom:5px;'></div>", unsafe_allow_html=True)
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"{count}", key=f"qc_a_{bucket}", use_container_width=True):
                            if count > 0:
                                st.session_state.page = 'aging_detail'
                                st.session_state.aging_zone = 'PK QC Center'
                                st.session_state.aging_bucket = bucket
                                st.rerun()
                st.markdown(f"<p style='color:#0F172A;font-weight:800;font-size:14px;margin-top:10px;'>Total: {len(qc_normal):,}</p>", unsafe_allow_html=True)
            
            with a3:
                st.markdown('**🚚 HANDOVER**', unsafe_allow_html=True)
                for bucket in BUCKET_ORDER:
                    count = handover_aging.get(bucket, 0)
                    st.markdown("<div style='border-bottom:1px solid #E2E8F0; margin-bottom:5px;'></div>", unsafe_allow_html=True)
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<span class='aging-bucket-text'>{bucket}</span>", unsafe_allow_html=True)
                    with c2:
                        if st.button(f"{count}", key=f"ho_a_{bucket}", use_container_width=True):
                            if count > 0:
                                st.session_state.page = 'handover_aging_detail'
                                st.session_state.handover_bucket = bucket
                                st.rerun()
                st.markdown(f"<p style='color:#0F172A;font-weight:800;font-size:14px;margin-top:10px;'>Total: {len(handover):,}</p>", unsafe_allow_html=True)

            # 5. PK ZONE VENDORS LIST (RESTORED!)
            st.markdown('<div class="section-header-saas">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
            pk_vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
            pk_vendor_counts.columns = ['Vendor', 'Orders']
            
            h1, h2, h3 = st.columns([5, 1, 2])
            with h1: st.markdown("<span class='vendor-header'>Vendor Name</span>", unsafe_allow_html=True)
            with h2: st.markdown("<span class='vendor-header'>Qty</span>", unsafe_allow_html=True)
            with h3: st.markdown("<span class='vendor-header'>Action/Comment</span>", unsafe_allow_html=True)
            
            for i, (_, row) in enumerate(pk_vendor_counts.iterrows()):
                vendor_key = f"pk_{row['Vendor']}"
                st.markdown("<div style='border-bottom: 1px solid #E2E8F0; margin-bottom: 5px;'></div>", unsafe_allow_html=True)
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
                    try: idx = VENDOR_ACTION_OPTIONS.index(current)
                    except: idx = 0
                    sel = st.selectbox("", VENDOR_ACTION_OPTIONS, index=idx, key=f"pa_{i}", label_visibility="collapsed")
                    if sel == '❌ Remove':
                        if vendor_key in st.session_state.vendor_comments: del st.session_state.vendor_comments[vendor_key]
                    elif sel != '--': st.session_state.vendor_comments[vendor_key] = sel

        # ---------------------------------------------------------
        # PAGE: 3PL SUMMARY
        # ---------------------------------------------------------
        elif st.session_state.page == '3pl_summary':
            st.markdown('<div class="page-main-title">3PL Performance Summary</div>', unsafe_allow_html=True)
            st.markdown('<div class="page-sub-title">Weekly executive overview across all logistics providers.</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 3])
            with c1:
                selected_date = st.date_input("Select Start Date (Monday)", value=datetime.today() - timedelta(days=datetime.today().weekday()))
            mon_date = selected_date - timedelta(days=selected_date.weekday())
            
            with st.spinner("Compiling global data (This may take a few seconds)..."):
                html_table = generate_3pl_html(mon_date)
                if html_table: st.markdown(html_table, unsafe_allow_html=True)
                else: st.warning("No data available for the selected week, or data is still loading.")

        # ---------------------------------------------------------
        # PAGE: DETAILS
        # ---------------------------------------------------------
        else:
            if st.button("← Back to Overview"): st.session_state.page = 'home'; st.rerun()
            
            pg = st.session_state.page
            if pg == 'handover': t, d = "🚚 Handover List", handover
            elif pg == 'pk_normal': t, d = "📍 PK Zone Normal", pk_normal
            elif pg == 'pk_ai': t, d = "🤖 PK Zone AI", pk_ai
            elif pg == 'qc_normal': t, d = "🏢 QC Center Normal", qc_normal
            elif pg == 'qc_ai': t, d = "🤖 QC Center AI", qc_ai
            elif pg == 'aging_detail':
                t, d = f"{'📍' if st.session_state.aging_zone == 'PK Zone' else '🏢'} {st.session_state.aging_zone} - {st.session_state.aging_bucket}", pk_normal[pk_normal['aging_bucket'] == st.session_state.aging_bucket] if st.session_state.aging_zone == 'PK Zone' else qc_normal[qc_normal['aging_bucket'] == st.session_state.aging_bucket]
            elif pg == 'vendor_detail':
                t, d = f"📍 Vendor: {st.session_state.vendor_name[:30]}", pk_normal[pk_normal['vendor'] == st.session_state.vendor_name] if st.session_state.vendor_zone == 'PK Zone' else qc_normal[qc_normal['vendor'] == st.session_state.vendor_name]
            elif pg == 'handover_aging_detail':
                t, d = f"🚚 Handover - {st.session_state.handover_bucket}", handover[handover['aging_bucket'] == st.session_state.handover_bucket]
            else: t, d = "Data View", approved
            
            st.markdown(f'<div class="page-main-title">{t}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="page-sub-title">{len(d):,} orders pending in this category.</div>', unsafe_allow_html=True)
            st.dataframe(d[DISPLAY_COLS], use_container_width=True, height=600)

except Exception as e:
    st.error("Connection Error: Unable to fetch data. Please try again.")
    st.write(e)
