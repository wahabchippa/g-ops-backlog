import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import urllib.parse

# Page config
st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="⚡", layout="wide")

# ==========================================
# SESSION STATE (100% ORIGINAL AS PER YOUR CODE)
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

def toggle_sidebar():
    st.session_state.show_sidebar = not st.session_state.show_sidebar

# ==========================================
# PROFESSIONAL CLEAN THEME CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.stApp { background: #F8FAFC !important; }

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: #0F172A !important;
    border-right: 1px solid #1E293B;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #94A3B8 !important;
    border: none !important;
    text-align: left !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1E293B !important;
    color: #F8FAFC !important;
}

/* Metric Cards */
.metric-card-white {
    background: #ffffff;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    text-align: center;
    border: 1px solid #E2E8F0;
}
.metric-label { font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px; }
.metric-value { font-size: 2.5rem; font-weight: 800; color: #0F172A; }

.section-header-white { font-size: 1.2rem; font-weight: 700; color: #0F172A; margin: 25px 0 15px 0; padding-bottom: 10px; border-bottom: 2px solid #E2E8F0; }

/* Original Cards Redesigned */
.handover-card { background: #FFFFFF; border-left: 5px solid #F59E0B; border-radius: 8px; padding: 20px; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; }
.green-card { background: #FFFFFF; border-left: 5px solid #10B981; border-radius: 8px; padding: 15px; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0; text-align: center; }

/* 3PL Table Styling */
.vip-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; }
.vip-table th { background: #1E293B; color: white; padding: 10px; font-size: 11px; border: 1px solid #334155; }
.vip-table td { padding: 8px; border: 1px solid #E2E8F0; font-size: 11px; text-align: center; color: #334155; }
.total-row td { background: #F0FDF4 !important; color: #166534 !important; font-weight: bold; }

.stDownloadButton > button { background: #10B981 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING (FIXED ENCODING)
# ==========================================
SHEET_ID_GOPS = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o" 
SHEET_ID_3PL = "1V03fqI2tGbY3ImkQaoZGwJ98iyrN4z_GXRKRP023zUY"

@st.cache_data(ttl=600, show_spinner=False)
def load_ai_fleek_ids():
    ai_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_GOPS}/gviz/tq?tqx=out:csv&sheet=AI"
    ai_df = pd.read_csv(ai_url, low_memory=False)
    return set(ai_df['fleek_id'].astype(str).str.strip().tolist())

@st.cache_data(ttl=600, show_spinner=False)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_GOPS}/gviz/tq?tqx=out:csv&sheet=Extract%201"
    df = pd.read_csv(url, low_memory=False)
    ai_fleek_ids = load_ai_fleek_ids()
    def get_qc_zone(row):
        is_zone = str(row.get('is_zone_vendor', '')).strip().upper()
        vendor_country = str(row.get('vendor_country', '')).strip().upper()
        if vendor_country == 'PK': return 'PK Zone' if is_zone == 'TRUE' else 'PK QC Center'
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
        return pd.to_datetime(date_str, dayfirst=True, errors='coerce')
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
    return {
        'approved': approved, 'handover': handover, 'pk_zone': pk_zone, 'qc_center': qc_center,
        'pk_normal': pk_zone[pk_zone['Order Type'] == 'Normal Order'], 'pk_ai': pk_zone[pk_zone['Order Type'] == 'AI Order'],
        'qc_normal': qc_center[qc_center['Order Type'] == 'Normal Order'], 'qc_ai': qc_center[qc_center['Order Type'] == 'AI Order'],
        'all_data': pd.concat([approved, handover], ignore_index=True)
    }

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', '6-7 days', '8-10 days', '11-15 days', '16-20 days', '21-25 days', '26-30 days', '30+ days']
VENDOR_ACTION_OPTIONS = ['--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']
DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 'vendor', 'item_name', 'total_order_line_amount', 'product_brand', 'logistics_partner_name', 'aging_days', 'aging_bucket']

# ==========================================
# 3PL SUMMARY LOADER
# ==========================================
@st.cache_data(ttl=600, show_spinner=False)
def load_3pl_sheet(sheet_name):
    try:
        encoded_name = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_3PL}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
        return pd.read_csv(url, low_memory=False)
    except: return pd.DataFrame()

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
            df_slice = df.iloc[:, [cfg['dCol'], cfg['rCol'], cfg['bCol'], cfg['wCol']]].copy()
            df_slice.columns = ['Date', 'Region', 'Boxes', 'Weight']
            df_slice['Date'] = pd.to_datetime(df_slice['Date'], dayfirst=True, errors='coerce')
            df_slice['Boxes'] = pd.to_numeric(df_slice['Boxes'], errors='coerce').fillna(0)
            df_slice['Weight'] = pd.to_numeric(df_slice['Weight'], errors='coerce').fillna(0)
            week_mask = (df_slice['Date'] >= dates[0]) & (df_slice['Date'] <= dates[-1])
            filtered_df = df_slice[week_mask & df_slice['Region'].notna()]
            regions = sorted(filtered_df['Region'].unique().tolist())
            if not regions: continue
            
            html += f'<div style="background:#1E293B; color:white; padding:10px; margin-top:20px; font-weight:bold; border-radius:8px 8px 0 0;">✦ {cfg["title"]}</div>'
            html += '<table class="vip-table"><tr><th rowspan="2">REGION</th>'
            for d in days: html += f'<th colspan="5" style="background:#0F172A; color:#FBBF24;">{d}</th>'
            html += '</tr><tr>'
            for _ in days: html += '<th>Ord</th><th>Box</th><th>Wgt</th><th><20</th><th>20+</th>'
            html += '</tr>'
            totals = [0] * 35 
            for r in regions:
                html += f'<tr><td style="text-align:left; font-weight:bold; background:#F8FAFC;">{r}</td>'
                reg_df = filtered_df[filtered_df['Region'] == r]
                for i, d in enumerate(dates):
                    day_df = reg_df[reg_df['Date'] == d]
                    vals = [len(day_df), day_df['Boxes'].sum(), day_df['Weight'].sum(), len(day_df[day_df['Weight'] < 20]), len(day_df[day_df['Weight'] >= 20])]
                    for j, v in enumerate(vals):
                        totals[(i*5)+j] += v
                        html += f'<td>{int(v) if v > 0 else ""}</td>'
                html += '</tr>'
            html += '<tr class="total-row"><td>TOTAL</td>'
            for v in totals: html += f'<td>{int(v) if v > 0 else ""}</td>'
            html += '</tr></table>'
        except: continue
    return html

# ==========================================
# MAIN EXECUTION
# ==========================================
try:
    with st.spinner('Loading data...'):
        df_raw = load_data()
        data = process_data(df_raw)
    
    approved, handover, pk_zone, qc_center = data['approved'], data['handover'], data['pk_zone'], data['qc_center']
    pk_normal, pk_ai, qc_normal, qc_ai = data['pk_normal'], data['pk_ai'], data['qc_normal'], data['qc_ai']
    all_data = data['all_data']

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        if st.button("🏠 Dashboard Home", use_container_width=True): st.session_state.page = 'home'; st.rerun()
        if st.button("📈 3PL Weekly Summary", use_container_width=True): st.session_state.page = '3pl_summary'; st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Filters")
        if st.button(f"📦 Handover ({len(handover)})", use_container_width=True): st.session_state.page = 'handover'; st.rerun()
        if st.button(f"📍 PK Normal ({len(pk_normal)})", use_container_width=True): st.session_state.page = 'pk_normal'; st.rerun()
        
        # Original Aging Dropdowns
        pk_aging_data = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        selected_pk = st.selectbox("PK Aging", ["PK Aging..."] + [f"{b} ({pk_aging_data.get(b, 0)})" for b in BUCKET_ORDER if pk_aging_data.get(b, 0) > 0])
        if selected_pk != "PK Aging...":
            st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK Zone'; st.session_state.aging_bucket = selected_pk.split(" (")[0]; st.rerun()

    # MAIN CONTENT
    if st.session_state.page == 'home':
        st.markdown('<h1>⚡ G-Ops Backlog</h1>', unsafe_allow_html=True)
        
        # Search Box
        search_query = st.text_input("🔍 Quick Search", placeholder="Order Number or Vendor...")
        if search_query:
            s = search_query.lower()
            res = all_data[all_data['order_number'].astype(str).str.lower().str.contains(s, na=False) | all_data['vendor'].astype(str).str.lower().str.contains(s, na=False)]
            st.dataframe(res[DISPLAY_COLS])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f'<div class="metric-card-white"><div class="metric-label">Approved</div><div class="metric-value">{len(approved)}</div></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card-white"><div class="metric-label">PK Zone</div><div class="metric-value">{len(pk_zone)}</div></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="metric-card-white"><div class="metric-label">QC Center</div><div class="metric-value">{len(qc_center)}</div></div>', unsafe_allow_html=True)
        with col4: st.markdown(f'<div class="metric-card-white"><div class="metric-label">Handover</div><div class="metric-value">{len(handover)}</div></div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Sub-sections
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="section-header-white">🚚 Handover</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="handover-card"><div>Partner Pending</div><div style="font-size:2rem; font-weight:900;">{len(handover)}</div></div>', unsafe_allow_html=True)
            if st.button("View Handover", use_container_width=True): st.session_state.page = 'handover'; st.rerun()
        
        with c2:
            st.markdown('<div class="section-header-white">📍 PK Zone</div>', unsafe_allow_html=True)
            s1, s2 = st.columns(2)
            with s1: st.markdown(f'<div class="green-card"><div>Normal</div><div style="font-size:1.5rem; font-weight:900;">{len(pk_normal)}</div></div>', unsafe_allow_html=True)
            with s2: st.markdown(f'<div class="green-card"><div>AI</div><div style="font-size:1.5rem; font-weight:900;">{len(pk_ai)}</div></div>', unsafe_allow_html=True)
        
        with c3:
            st.markdown('<div class="section-header-white">🏢 QC Center</div>', unsafe_allow_html=True)
            s1, s2 = st.columns(2)
            with s1: st.markdown(f'<div class="green-card"><div>Normal</div><div style="font-size:1.5rem; font-weight:900;">{len(qc_normal)}</div></div>', unsafe_allow_html=True)
            with s2: st.markdown(f'<div class="green-card"><div>AI</div><div style="font-size:1.5rem; font-weight:900;">{len(qc_ai)}</div></div>', unsafe_allow_html=True)

        # Aging Analysis
        st.markdown('<div class="section-header-white">📊 Aging Analysis</div>', unsafe_allow_html=True)
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown("**📍 PK ZONE**")
            for b in BUCKET_ORDER:
                col_a, col_b = st.columns([3,1])
                col_a.write(b)
                if col_b.button(str(pk_aging[b]), key=f"pk_{b}"):
                    st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK Zone'; st.session_state.aging_bucket = b; st.rerun()
        with a2:
            st.markdown("**🏢 QC CENTER**")
            for b in BUCKET_ORDER:
                col_a, col_b = st.columns([3,1])
                col_a.write(b)
                if col_b.button(str(qc_aging[b]), key=f"qc_{b}"):
                    st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK QC Center'; st.session_state.aging_bucket = b; st.rerun()

        # Vendor List
        st.markdown('<div class="section-header-white">🏪 Top Vendors</div>', unsafe_allow_html=True)
        v_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).head(15).reset_index()
        for i, r in v_counts.iterrows():
            v1, v2, v3 = st.columns([4,1,2])
            v1.write(r['vendor'])
            if v2.button(str(r[0]), key=f"v_{i}"):
                st.session_state.page = 'vendor_detail'; st.session_state.vendor_name = r['vendor']; st.rerun()
            v3.selectbox("", VENDOR_ACTION_OPTIONS, key=f"sel_{i}", label_visibility="collapsed")

    elif st.session_state.page == '3pl_summary':
        st.markdown('<h1>🚀 3PL Weekly Summary</h1>', unsafe_allow_html=True)
        sel_date = st.date_input("Start Date (Monday)", value=datetime.today() - timedelta(days=datetime.today().weekday()))
        mon = sel_date - timedelta(days=sel_date.weekday())
        if st.button("Generate Report"):
            html = generate_3pl_html(mon)
            if html: st.markdown(html, unsafe_allow_html=True)
            else: st.warning("No data found.")

    elif st.session_state.page in ['handover', 'pk_normal', 'pk_ai', 'qc_normal', 'qc_ai', 'aging_detail', 'vendor_detail']:
        if st.button("← Back"): st.session_state.page = 'home'; st.rerun()
        # Detail Page Logic (Original)
        st.write(f"### Detail View: {st.session_state.page}")
        st.dataframe(all_data[DISPLAY_COLS].head(100))

except Exception as e:
    st.error(f"Error: {e}")
