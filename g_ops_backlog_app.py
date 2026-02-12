import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Page config
st.set_page_config(
    page_title="G-Ops Backlog Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean Professional Theme - Light main, Dark detail pages
def get_css():
    if st.session_state.get('page', 'home') == 'home':
        # Light theme for home
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        .stApp {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Main Title */
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0;
        }
        
        .subtitle {
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 5px;
        }
        
        /* Section Headings */
        .section-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1a1a2e;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #dee2e6;
        }
        
        /* Metric Cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
            text-align: center;
        }
        
        .metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a2e;
            margin-top: 5px;
        }
        
        /* Buttons - Light with hover */
        .stButton > button {
            background: white !important;
            color: #1a1a2e !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 8px !important;
            padding: 8px 20px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background: #1a1a2e !important;
            color: white !important;
            border-color: #1a1a2e !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(26,26,46,0.2);
        }
        
        /* Tables */
        .aging-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .aging-table table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .aging-table th {
            background: #1a1a2e;
            color: white;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
        }
        
        .aging-table td {
            padding: 10px 16px;
            border-bottom: 1px solid #e9ecef;
            color: #333;
        }
        
        .aging-table tr:hover {
            background: #f8f9fa;
        }
        
        .aging-table tr:last-child td {
            border-bottom: none;
            font-weight: 600;
            background: #f1f3f4;
        }
        
        /* Info cards */
        .info-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #0f3460;
        }
        
        .info-title {
            font-weight: 600;
            color: #1a1a2e;
            font-size: 1rem;
        }
        
        .info-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0f3460;
        }
        
        /* Hide streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Divider */
        hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 30px 0;
        }
        </style>
        """
    else:
        # Dark theme for detail pages
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        /* Page Title */
        .page-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 5px;
        }
        
        .page-subtitle {
            color: #8892a0;
            font-size: 0.9rem;
        }
        
        /* Back Button */
        .stButton > button {
            background: transparent !important;
            color: #4dabf7 !important;
            border: 1px solid #4dabf7 !important;
            border-radius: 8px !important;
            padding: 8px 20px !important;
            font-weight: 500 !important;
        }
        
        .stButton > button:hover {
            background: #4dabf7 !important;
            color: #0a0a0f !important;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background: #1e2a3a !important;
            color: white !important;
            border: 1px solid #2d3a4a !important;
            border-radius: 8px !important;
        }
        
        .stSelectbox > div > div {
            background: #1e2a3a !important;
            color: white !important;
            border-radius: 8px !important;
        }
        
        /* Labels */
        .stTextInput label, .stSelectbox label {
            color: #8892a0 !important;
        }
        
        /* Dataframe */
        .stDataFrame {
            background: #141b27;
            border-radius: 12px;
            overflow: hidden;
        }
        
        [data-testid="stDataFrame"] {
            background: #141b27;
        }
        
        /* Download button */
        .stDownloadButton > button {
            background: #28a745 !important;
            color: white !important;
            border: none !important;
        }
        
        .stDownloadButton > button:hover {
            background: #218838 !important;
        }
        
        /* Text colors */
        p, span, label { color: #e9ecef; }
        
        /* Hide streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        </style>
        """

# Session state init
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Apply CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Data loading
@st.cache_data(ttl=300)
def load_data():
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]
        )
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key("1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o")
        worksheet = sheet.worksheet("Dump")
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Parse date
def parse_date(date_str):
    if pd.isna(date_str) or date_str == '' or date_str == 'FALSE':
        return None
    try:
        return pd.to_datetime(date_str, format='%B %d, %Y, %H:%M')
    except:
        try:
            return pd.to_datetime(date_str)
        except:
            return None

# Get aging bucket
def get_aging_bucket(days):
    if pd.isna(days) or days < 0:
        return None
    if days <= 5:
        return f"{int(days)} day" if days == 1 else f"{int(days)} days"
    elif days <= 7:
        return "6-7 days"
    elif days <= 10:
        return "8-10 days"
    elif days <= 15:
        return "11-15 days"
    elif days <= 20:
        return "16-20 days"
    elif days <= 25:
        return "21-25 days"
    elif days <= 30:
        return "26-30 days"
    else:
        return "30+ days"

BUCKET_ORDER = ['0 days', '1 day', '2 days', '3 days', '4 days', '5 days', 
                '6-7 days', '8-10 days', '11-15 days', '16-20 days', 
                '21-25 days', '26-30 days', '30+ days']

# Load data
df = load_data()

if df.empty:
    st.error("No data available")
    st.stop()

# Process data
approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
approved['aging_days'] = approved['qc_date'].apply(
    lambda x: (datetime.now() - x).days if x else None
)
approved['aging_bucket'] = approved['aging_days'].apply(get_aging_bucket)

handover = df[
    (df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
    (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))
].copy()
handover['handover_date'] = handover['logistics_partner_handedover_at'].apply(parse_date)
handover['aging_days'] = handover['handover_date'].apply(
    lambda x: (datetime.now() - x).days if x else None
)
handover['aging_bucket'] = handover['aging_days'].apply(get_aging_bucket)

# Filter data
pk_zone = approved[approved['QC or zone'] == 'PK Zone']
qc_center = approved[approved['QC or zone'] == 'PK QC Center']
pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']

# Display columns for detail pages
DISPLAY_COLS = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                'vendor', 'item_name', 'total_order_line_amount', 'product_brand',
                'logistics_partner_name', 'aging_days', 'aging_bucket']

# ==================== PAGES ====================

def show_home():
    # Title with icon
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 5px;">
            <span style="font-size: 3rem;">📦</span>
            <span class="main-title">G-Ops Backlog Dashboard</span>
        </div>
        <p class="subtitle">✨ Last updated: """ + datetime.now().strftime("%d %b %Y, %I:%M %p") + """</p>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Approved</div>
                <div class="metric-value">{len(approved):,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">PK Zone</div>
                <div class="metric-value">{len(pk_zone):,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">QC Center</div>
                <div class="metric-value">{len(qc_center):,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Handover</div>
                <div class="metric-value">{len(handover):,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Handover Section
    st.markdown('<p class="section-header">🚚 Handover to Logistics</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 3])
    with col1:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">Orders handed over to logistics partner</div>
                <div class="info-value">{len(handover):,} orders</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("View Handover Orders", key="view_handover"):
            st.session_state.page = 'handover_list'
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # PK Zone Orders
    st.markdown('<p class="section-header">📍 PK Zone Orders</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">Normal Orders</div>
                <div class="info-value">{len(pk_normal):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("View", key="view_pk_normal"):
            st.session_state.page = 'pk_normal'
            st.rerun()
    with col3:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">AI Orders</div>
                <div class="info-value">{len(pk_ai):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        if st.button("View", key="view_pk_ai"):
            st.session_state.page = 'pk_ai'
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # QC Center Orders
    st.markdown('<p class="section-header">🏢 QC Center Orders</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">Normal Orders</div>
                <div class="info-value">{len(qc_normal):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("View", key="view_qc_normal"):
            st.session_state.page = 'qc_normal'
            st.rerun()
    with col3:
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">AI Orders</div>
                <div class="info-value">{len(qc_ai):,}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        if st.button("View", key="view_qc_ai"):
            st.session_state.page = 'qc_ai'
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Aging Analysis Tables
    st.markdown('<p class="section-header">📊 Aging Analysis - Normal Orders</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # PK Zone Aging Table
    with col1:
        st.markdown("**📍 PK Zone Normal**")
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        table_html = """
        <div class="aging-table">
            <table>
                <tr><th>Aging</th><th style="text-align:right;">Count</th></tr>
        """
        for bucket in BUCKET_ORDER:
            count = pk_aging.get(bucket, 0)
            table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
        table_html += f"<tr><td><strong>Total</strong></td><td style='text-align:right;'><strong>{len(pk_normal)}</strong></td></tr>"
        table_html += "</table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
    
    # QC Center Aging Table
    with col2:
        st.markdown("**🏢 QC Center Normal**")
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        table_html = """
        <div class="aging-table">
            <table>
                <tr><th>Aging</th><th style="text-align:right;">Count</th></tr>
        """
        for bucket in BUCKET_ORDER:
            count = qc_aging.get(bucket, 0)
            table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
        table_html += f"<tr><td><strong>Total</strong></td><td style='text-align:right;'><strong>{len(qc_normal)}</strong></td></tr>"
        table_html += "</table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Vendor Table
    st.markdown('<p class="section-header">🏪 PK Zone Vendors - Normal Orders</p>', unsafe_allow_html=True)
    
    vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
    vendor_counts.columns = ['Vendor', 'Orders']
    
    st.markdown("""
        <div class="aging-table">
            <table>
                <tr><th>Vendor</th><th style="text-align:right;">Orders</th></tr>
    """ + "".join([f"<tr><td>{row['Vendor']}</td><td style='text-align:right;'>{row['Orders']}</td></tr>" 
                   for _, row in vendor_counts.iterrows()]) + 
    f"<tr><td><strong>Total ({len(vendor_counts)} vendors)</strong></td><td style='text-align:right;'><strong>{len(pk_normal)}</strong></td></tr>"
    + "</table></div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Handover Aging
    st.markdown('<p class="section-header">🚚 Handover Aging Analysis</p>', unsafe_allow_html=True)
    
    handover_aging = handover.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
    
    table_html = """
    <div class="aging-table">
        <table>
            <tr><th>Aging</th><th style="text-align:right;">Count</th></tr>
    """
    for bucket in BUCKET_ORDER:
        count = handover_aging.get(bucket, 0)
        table_html += f"<tr><td>{bucket}</td><td style='text-align:right;'>{count}</td></tr>"
    table_html += f"<tr><td><strong>Total</strong></td><td style='text-align:right;'><strong>{len(handover)}</strong></td></tr>"
    table_html += "</table></div>"
    st.markdown(table_html, unsafe_allow_html=True)


def show_detail_page(data, title, subtitle):
    # Back button
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f'<p class="page-title">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{subtitle} • {len(data):,} orders</p>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search = st.text_input("🔍 Search", placeholder="Order number, customer, vendor...")
    with col2:
        countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
        country = st.selectbox("🌍 Country", countries)
    with col3:
        st.write("")
        st.write("")
        csv = data.to_csv(index=False)
        st.download_button("📥 Export CSV", csv, f"{title.lower().replace(' ', '_')}.csv", "text/csv")
    
    # Apply filters
    filtered = data.copy()
    if search:
        search_lower = search.lower()
        filtered = filtered[
            filtered['order_number'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered['customer_name'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered['vendor'].astype(str).str.lower().str.contains(search_lower, na=False) |
            filtered['fleek_id'].astype(str).str.lower().str.contains(search_lower, na=False)
        ]
    if country != 'All':
        filtered = filtered[filtered['customer_country'] == country]
    
    # Display table
    display_df = filtered[[c for c in DISPLAY_COLS if c in filtered.columns]].copy()
    st.dataframe(display_df, use_container_width=True, height=600)


# ==================== ROUTING ====================

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'pk_normal':
    show_detail_page(pk_normal, "PK Zone - Normal Orders", "QC Approved orders from PK Zone")
elif st.session_state.page == 'pk_ai':
    show_detail_page(pk_ai, "PK Zone - AI Orders", "QC Approved AI orders from PK Zone")
elif st.session_state.page == 'qc_normal':
    show_detail_page(qc_normal, "QC Center - Normal Orders", "QC Approved orders from QC Center")
elif st.session_state.page == 'qc_ai':
    show_detail_page(qc_ai, "QC Center - AI Orders", "QC Approved AI orders from QC Center")
elif st.session_state.page == 'handover_list':
    show_detail_page(handover, "Handover Orders", "Orders handed over to logistics partner")
else:
    st.session_state.page = 'home'
    st.rerun()
