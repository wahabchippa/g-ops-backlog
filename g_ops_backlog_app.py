import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="📦", layout="wide")

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Dynamic Theme based on page
if st.session_state.page == 'home':
    # LIGHT THEME for Home
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(145deg, #ffffff 0%, #f5f7fa 50%, #e8ecf1 100%);
    }
    
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Beautiful Title */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Dark Section Headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1e293b;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
    }
    
    /* Light Buttons with Hover Effect */
    .stButton > button {
        background: white !important;
        color: #475569 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: white !important;
        border-color: #1e293b !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30,41,59,0.25);
    }
    
    /* Clean Tables */
    .aging-table {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }
    
    .aging-table table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .aging-table th {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 14px 20px;
        text-align: left;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .aging-table td {
        padding: 12px 20px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
        font-size: 0.95rem;
    }
    
    .aging-table tr:hover {
        background: #f8fafc;
    }
    
    .aging-table tr:last-child td {
        border-bottom: none;
        font-weight: 700;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #1e293b;
    }
    
    /* Info Cards */
    .info-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid;
        border-image: linear-gradient(180deg, #667eea 0%, #764ba2 100%) 1;
    }
    
    .info-title {
        font-weight: 600;
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .info-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #e2e8f0;
        margin: 35px 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
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
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 20px rgba(96,165,250,0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
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

# Data Loading
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
    return pd.read_csv(url, low_memory=False)

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%B %d, %Y, %H:%M')
    except:
        return pd.NaT

def get_aging_bucket(days):
    if pd.isna(days) or days < 0: return None
    if days == 0: return "0 days"
    if days == 1: return "1 day"
    if days <= 5: return f"{int(days)} days"
    elif days <= 7: return "6-7 days"
    elif days <= 10: return "8-10 days"
    elif days <= 15: return "11-15 days"
    elif days <= 20: return "16-20 days"
    elif days <= 25: return "21-25 days"
    elif days <= 30: return "26-30 days"
    else: return "30+ days"

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                '6-7 days', '8-10 days', '11-15 days', '16-20 days', 
                '21-25 days', '26-30 days', '30+ days']

try:
    df = load_data()
    
    # Process Data
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))].copy()
    
    approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
    approved['aging_days'] = (datetime.now() - approved['qc_date']).dt.days
    approved['aging_bucket'] = approved['aging_days'].apply(get_aging_bucket)
    
    handover['handover_date'] = handover['logistics_partner_handedover_at'].apply(parse_date)
    handover['aging_days'] = (datetime.now() - handover['handover_date']).dt.days
    handover['aging_bucket'] = handover['aging_days'].apply(get_aging_bucket)
    
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
    pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
    qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
    qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']
    
    DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                    'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
                    'logistics_partner_name', 'aging_days', 'aging_bucket']

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
        
        # Aging Analysis Tables
        st.markdown('<div class="section-header">📊 Aging Analysis - Normal Orders</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # PK Zone Aging
        with col1:
            st.markdown("##### 📍 PK Zone Normal")
            pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            table_html = '<div class="aging-table"><table><tr><th>Aging</th><th style="text-align:right;">Count</th></tr>'
            for bucket in BUCKET_ORDER:
                count = pk_aging.get(bucket, 0)
                table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
            table_html += f"<tr><td>Total</td><td style='text-align:right;'>{len(pk_normal):,}</td></tr></table></div>"
            st.markdown(table_html, unsafe_allow_html=True)
        
        # QC Center Aging
        with col2:
            st.markdown("##### 🏢 QC Center Normal")
            qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
            table_html = '<div class="aging-table"><table><tr><th>Aging</th><th style="text-align:right;">Count</th></tr>'
            for bucket in BUCKET_ORDER:
                count = qc_aging.get(bucket, 0)
                table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
            table_html += f"<tr><td>Total</td><td style='text-align:right;'>{len(qc_normal):,}</td></tr></table></div>"
            st.markdown(table_html, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Vendor Table
        st.markdown('<div class="section-header">🏪 PK Zone Vendors - Normal Orders</div>', unsafe_allow_html=True)
        vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        vendor_counts.columns = ['Vendor', 'Orders']
        
        table_html = '<div class="aging-table"><table><tr><th>Vendor</th><th style="text-align:right;">Orders</th></tr>'
        for _, row in vendor_counts.iterrows():
            table_html += f"<tr><td>{row['Vendor']}</td><td style='text-align:right;'>{row['Orders']}</td></tr>"
        table_html += f"<tr><td>Total ({len(vendor_counts)} vendors)</td><td style='text-align:right;'>{len(pk_normal):,}</td></tr></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Handover Aging
        st.markdown('<div class="section-header">🚚 Handover Aging Analysis</div>', unsafe_allow_html=True)
        handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        table_html = '<div class="aging-table"><table><tr><th>Aging</th><th style="text-align:right;">Count</th></tr>'
        for bucket in BUCKET_ORDER:
            count = handover_aging.get(bucket, 0)
            table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
        table_html += f"<tr><td>Total</td><td style='text-align:right;'>{len(handover):,}</td></tr></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)

    # ==================== DETAIL PAGES (DARK) ====================
    else:
        # Back Button
        if st.button("← Back to Dashboard", key="back"):
            st.session_state.page = 'home'
            st.rerun()
        
        st.write("")
        
        # Determine which page
        page = st.session_state.page
        if page == 'handover':
            title, data = "🚚 Handover Orders", handover
        elif page == 'pk_normal':
            title, data = "📍 PK Zone - Normal Orders", pk_normal
        elif page == 'pk_ai':
            title, data = "📍 PK Zone - AI Orders", pk_ai
        elif page == 'qc_normal':
            title, data = "🏢 QC Center - Normal Orders", qc_normal
        elif page == 'qc_ai':
            title, data = "🏢 QC Center - AI Orders", qc_ai
        else:
            title, data = "📋 Orders", approved
        
        # Page Header
        st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">📋 {len(data):,} orders found</div>', unsafe_allow_html=True)
        
        st.write("")
        
        # Filters Row
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order number, customer name, vendor...")
        with col2:
            countries = ['All Countries'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Filter by Country", countries)
        with col3:
            st.write(""); st.write("")
            st.download_button("📥 Export CSV", data.to_csv(index=False), "orders.csv", "text/csv", use_container_width=True)
        
        st.write("")
        
        # Apply Filters
        filtered = data.copy()
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
        
        # Results count
        st.markdown(f'<p style="color: #94a3b8; margin-bottom: 10px;">Showing {len(filtered):,} of {len(data):,} orders</p>', unsafe_allow_html=True)
        
        # Data Table
        display_df = filtered[[c for c in DISPLAY_COLS if c in filtered.columns]]
        st.dataframe(display_df, use_container_width=True, height=600)

except Exception as e:
    st.error(f"Error loading data: {e}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
