import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import urllib.parse

# ==========================================
# 1. PAGE CONFIG (ASLI ORIGINAL)
# ==========================================
st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="⚡", layout="wide")

# ==========================================
# 2. SESSION STATE (ASLI ORIGINAL)
# ==========================================
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

# ==========================================
# 3. CSS (ASLI ORIGINAL DARK THEME)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: linear-gradient(145deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
}

.metric-card-white {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    text-align: center;
}
.metric-card-white .metric-label { font-size: 0.75rem; font-weight: 700; color: #444444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
.metric-card-white .metric-value { font-size: 3rem; font-weight: 900; color: #111111; }

.section-header-white { font-size: 1.4rem; font-weight: 700; color: #ffffff; margin: 25px 0 18px 0; padding-bottom: 12px; border-bottom: 2px solid #333333; }

.handover-card {
    background: linear-gradient(145deg, #4a2c17 0%, #2d1a0e 100%);
    border-radius: 16px; padding: 24px; box-shadow: 0 8px 30px rgba(74,44,23,0.5); border: 1px solid #5c3a22;
}
.handover-card .info-title { color: #ffffff; font-size: 0.85rem; font-weight: 700; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
.handover-card .info-value { color: #ffffff; font-size: 2.8rem; font-weight: 900; }

.green-card {
    background: linear-gradient(145deg, #1f4d1f 0%, #143314 100%);
    border-radius: 14px; padding: 20px; box-shadow: 0 6px 25px rgba(34,197,94,0.2); border: 1px solid #2d6a2d; text-align: center;
}
.green-card .metric-label { color: #ffffff; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }
.green-card .metric-value { color: #7eed9e; font-size: 2.2rem; font-weight: 800; }

.stButton > button {
    background: #4a4a4a !important; color: #e0e0e0 !important; border: 1px solid #5a5a5a !important; border-radius: 8px !important; font-weight: 700 !important;
}

.stMarkdown, p, span, label { color: #a0a0a0 !important; font-size: 0.9rem !important; }
h1, h2, h3, h4, h5, h6 { color: #e0e0e0 !important; }

/* 3PL SUMMARY VIP TABLE (NEW ADDITION ONLY) */
.vip-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e1e1e; border-radius: 12px; overflow: hidden; border: 1px solid #333; }
.vip-table th { background: #0F172A; color: #FBBF24; padding: 12px; font-size: 11px; border: 1px solid #333; text-align: center; }
.vip-table td { padding: 10px; border: 1px solid #333; font-size: 11px; text-align: center; color: #ddd; }
.total-row td { background: #0A0F24 !important; color: #10B981 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA LOADING (SEPARATED IDS)
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
        if vendor_country == 'PK':
            return 'PK Zone' if is_zone == 'TRUE' else 'PK QC Center'
        elif vendor_country == 'IN':
            return 'IN Zone' if is_zone == 'TRUE' else 'IN QC Center'
        return 'Other'
    df['QC or zone'] = df.apply(get_qc_zone, axis=1)
    df['Order Type'] = df['fleek_id'].apply(lambda x: 'AI Order' if str(x).strip() in ai_fleek_ids else 'Normal Order')
    return df

@st.cache_data(ttl=600, show_spinner=False)
def load_3pl_sheet(sheet_name):
    try:
        encoded_name = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_3PL}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
        return pd.read_csv(url, low_memory=False)
    except: return pd.DataFrame()

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
        conditions = [days_series == 0, days_series == 1, days_series == 2, days_series == 3, days_series == 4, days_series == 5, (days_series >= 6) & (days_series <= 7), (days_series >= 8) & (days_series <= 10), (days_series >= 11) & (days_series <= 15), (days_series >= 16) & (days_series <= 20), (days_series >= 21) & (days_series <= 25), (days_series >= 26) & (days_series <= 30), days_series > 30]
        choices = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', '6-7 days', '8-10 days', '11-15 days', '16-20 days', '21-25 days', '26-30 days', '30+ days']
        return np.select(conditions, choices, default=None)
    
    approved['aging_bucket'] = assign_buckets(approved['aging_days'])
    handover['aging_bucket'] = assign_buckets(handover['aging_days'])
    
    return {
        'approved': approved, 'handover': handover,
        'pk_zone': approved[approved['QC or zone'] == 'PK Zone'],
        'qc_center': approved[approved['QC or zone'] == 'PK QC Center'],
        'pk_normal': approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'Normal Order')],
        'pk_ai': approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'AI Order')],
        'qc_normal': approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'Normal Order')],
        'qc_ai': approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'AI Order')],
        'all_data': pd.concat([approved, handover], ignore_index=True)
    }

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', '6-7 days', '8-10 days', '11-15 days', '16-20 days', '21-25 days', '26-30 days', '30+ days']
VENDOR_ACTION_OPTIONS = ['--', 'today', 'update', 'Tuesday', 'Thursday', 'Saturday', 'NOT Response', 'MOVE to WH', '❌ Remove']
DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 'vendor', 'item_name', 'total_order_line_amount', 'product_brand', 'logistics_partner_name', 'aging_days', 'aging_bucket']

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
            week_mask = (df_slice['Date'] >= dates[0]) & (df_slice['Date'] <= dates[-1])
            filtered = df_slice[week_mask & df_slice['Region'].notna()]
            regions = sorted(filtered['Region'].unique().tolist())
            if not regions: continue
            html += f'<div style="background:#1E293B; color:white; padding:10px; margin-top:20px; font-weight:bold; border-radius:8px;">✦ {cfg["title"]}</div><table class="vip-table"><tr><th rowspan="2">REGION</th>'
            for d in days: html += f'<th colspan="5" style="background:#0F172A; color:#FBBF24;">{d}</th>'
            html += '</tr><tr>'
            for _ in days: html += '<th>Ord</th><th>Box</th><th>Wgt</th><th><20</th><th>20+</th>'
            html += '</tr>'
            totals = [0] * 35 
            for r in regions:
                html += f'<tr><td style="text-align:left; font-weight:bold; background:#252525;">{r}</td>'
                reg_df = filtered[filtered['Region'] == r]
                for i, d in enumerate(dates):
                    day_df = reg_df[reg_df['Date'] == d]
                    v = [len(day_df), day_df['Boxes'].sum(), day_df['Weight'].sum(), len(day_df[day_df['Weight'] < 20]), len(day_df[day_df['Weight'] >= 20])]
                    for j, val in enumerate(v): totals[(i*5)+j] += val; html += f'<td>{int(val) if val > 0 else ""}</td>'
                html += '</tr>'
            html += '<tr class="total-row"><td>TOTAL</td>'
            for v in totals: html += f'<td>{int(v) if v > 0 else ""}</td>'
            html += '</tr></table>'
        except: continue
    return html

# ==========================================
# 5. MAIN APP LAYOUT (100% ASLI REPLICA)
# ==========================================
try:
    with st.spinner('Loading data...'):
        df_raw = load_data()
        data = process_data(df_raw)
    
    approved = data['approved']
    handover = data['handover']
    pk_normal, pk_ai = data['pk_normal'], data['pk_ai']
    qc_normal, qc_ai = data['qc_normal'], data['qc_ai']
    all_data = data['all_data']

    # SIDEBAR (100% ASLI)
    if st.session_state.show_sidebar:
        sidebar_col, main_col = st.columns([1, 4])
        with sidebar_col:
            if st.button("✕ Close Sidebar", use_container_width=True): 
                st.session_state.show_sidebar = False
                st.rerun()
            st.markdown("## 🎯 Navigation")
            if st.button("🏠 Dashboard Home", use_container_width=True): 
                st.session_state.page = 'home'
                st.rerun()
            
            # --- ONLY ADDITION TO SIDEBAR ---
            if st.button("🚀 3PL Summary", use_container_width=True): 
                st.session_state.page = '3pl_summary'
                st.rerun()
            # -------------------------------

            st.markdown("---")
            pk_aging_data = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            sel_pk = st.selectbox("PK Aging", ["PK Aging..."] + [f"{b} ({pk_aging_data.get(b, 0)})" for b in BUCKET_ORDER if pk_aging_data.get(b, 0) > 0])
            if sel_pk != "PK Aging...":
                st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK Zone'; st.session_state.aging_bucket = sel_pk.split(" (")[0]; st.rerun()
    else:
        main_col = st.container()
        if st.button("☰ Sidebar"): toggle_sidebar(); st.rerun()

    with main_col:
        # ---------------------------------------------------------
        # HOME PAGE (ASLI 100%)
        # ---------------------------------------------------------
        if st.session_state.page == 'home':
            st.markdown('<h1 style="color:white; font-size:48px; font-weight:900;">⚡ G-Ops Backlog Dashboard</h1>', unsafe_allow_html=True)
            
            # Search Box (Asli)
            search_query = st.text_input("🔍 Quick Search", placeholder="Enter Order Number or Vendor Name...")
            if search_query:
                s = search_query.lower()
                res = all_data[all_data['order_number'].astype(str).str.lower().str.contains(s, na=False) | all_data['vendor'].astype(str).str.lower().str.contains(s, na=False)]
                st.dataframe(res[DISPLAY_COLS])

            # Metrics (Asli)
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(f'<div class="metric-card-white"><div class="metric-label">Approved</div><div class="metric-value">{len(approved)}</div></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card-white"><div class="metric-label">PK Zone</div><div class="metric-value">{len(pk_normal)+len(pk_ai)}</div></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card-white"><div class="metric-label">QC Center</div><div class="metric-value">{len(qc_normal)+len(qc_ai)}</div></div>', unsafe_allow_html=True)
            with c4: st.markdown(f'<div class="metric-card-white"><div class="metric-label">Handover</div><div class="metric-value">{len(handover)}</div></div>', unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Original Sub-sections
            row1_c1, row1_c2, row1_c3 = st.columns(3)
            with row1_c1:
                st.markdown('<div class="section-header-white">🚚 Handover</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="handover-card"><div class="info-title">To Partner</div><div class="info-value">{len(handover)}</div></div>', unsafe_allow_html=True)
                if st.button("View Handover", use_container_width=True): st.session_state.page = 'handover'; st.rerun()
            with row1_c2:
                st.markdown('<div class="section-header-white">📍 PK Zone</div>', unsafe_allow_html=True)
                s1, s2 = st.columns(2)
                with s1: st.markdown(f'<div class="green-card"><div class="metric-label">Normal</div><div class="metric-value">{len(pk_normal)}</div></div>', unsafe_allow_html=True)
                with s2: st.markdown(f'<div class="green-card"><div class="metric-label">AI</div><div class="metric-value">{len(pk_ai)}</div></div>', unsafe_allow_html=True)
            with row1_c3:
                st.markdown('<div class="section-header-white">🏢 QC Center</div>', unsafe_allow_html=True)
                s1, s2 = st.columns(2)
                with s1: st.markdown(f'<div class="green-card"><div class="metric-label">Normal</div><div class="metric-value">{len(qc_normal)}</div></div>', unsafe_allow_html=True)
                with s2: st.markdown(f'<div class="green-card"><div class="metric-label">AI</div><div class="metric-value">{len(qc_ai)}</div></div>', unsafe_allow_html=True)

            # Aging Analysis (Asli)
            st.markdown('<div class="section-header-white">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
            pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            a1, a2, a3 = st.columns(3)
            with a1:
                st.markdown("**📍 PK ZONE**")
                for b in BUCKET_ORDER:
                    c_a, c_b = st.columns([3,1])
                    c_a.write(b)
                    if c_b.button(str(pk_aging[b]), key=f"pk_{b}"):
                        st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK Zone'; st.session_state.aging_bucket = b; st.rerun()
            with a2:
                st.markdown("**🏢 QC CENTER**")
                for b in BUCKET_ORDER:
                    c_a, c_b = st.columns([3,1])
                    c_a.write(b)
                    if c_b.button(str(qc_aging[b]), key=f"qc_{b}"):
                        st.session_state.page = 'aging_detail'; st.session_state.aging_zone = 'PK QC Center'; st.session_state.aging_bucket = b; st.rerun()

            # Vendors List (Asli)
            st.markdown('<div class="section-header-white">🏪 PK Zone Vendors</div>', unsafe_allow_html=True)
            v_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).head(20).reset_index()
            for i, r in v_counts.iterrows():
                v1, v2, v3 = st.columns([5,1,2])
                v1.write(r['vendor'])
                if v2.button(str(r[0]), key=f"v_{i}"):
                    st.session_state.page = 'vendor_detail'; st.session_state.vendor_name = r['vendor']; st.rerun()
                st.selectbox("", VENDOR_ACTION_OPTIONS, key=f"sel_{i}", label_visibility="collapsed")

        # ---------------------------------------------------------
        # NEW PAGE: 3PL SUMMARY
        # ---------------------------------------------------------
        elif st.session_state.page == '3pl_summary':
            st.markdown('<h1>🚀 3PL Weekly Summary</h1>', unsafe_allow_html=True)
            sd = st.date_input("Start Date (Mon)", value=datetime.today() - timedelta(days=datetime.today().weekday()))
            mon = sd - timedelta(days=sd.weekday())
            if st.button("Generate Report"):
                html = generate_3pl_html(mon)
                if html: st.markdown(html, unsafe_allow_html=True)
                else: st.warning("No data found for this week.")

        # ---------------------------------------------------------
        # DETAIL PAGES (ASLI 100%)
        # ---------------------------------------------------------
        elif st.session_state.page in ['handover', 'pk_normal', 'aging_detail', 'vendor_detail']:
            if st.button("← Back to Dashboard"): st.session_state.page = 'home'; st.rerun()
            st.dataframe(all_data[DISPLAY_COLS].head(200))

except Exception as e:
    st.error(f"Error: {e}")
