import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="G-Ops Backlog Dashboard",
    page_icon="📦",
    layout="wide"
)

# MUI Light Theme CSS
st.markdown("""
<style>
    /* Import Roboto font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Force Light Theme */
    .stApp {
        background-color: #f5f5f5 !important;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Override dark theme */
    .main .block-container {
        background-color: #f5f5f5 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #f5f5f5 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #1976d2 !important;
    }
    
    /* MUI App Bar */
    .mui-appbar {
        background: linear-gradient(90deg, #1976d2 0%, #1565c0 100%);
        padding: 20px 24px;
        border-radius: 0 0 8px 8px;
        margin: -1rem -1rem 24px -1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .mui-appbar-title {
        font-size: 26px;
        font-weight: 500;
        color: #ffffff;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .mui-appbar-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.8);
        margin-top: 4px;
    }
    
    /* MUI Card */
    .mui-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        transition: box-shadow 0.2s ease;
    }
    
    .mui-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.12), 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* MUI Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        border-radius: 8px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-card.purple {
        background: linear-gradient(135deg, #7b1fa2 0%, #6a1b9a 100%);
        box-shadow: 0 4px 12px rgba(123, 31, 162, 0.25);
    }
    
    .metric-card.green {
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%);
        box-shadow: 0 4px 12px rgba(56, 142, 60, 0.25);
    }
    
    .metric-card.orange {
        background: linear-gradient(135deg, #f57c00 0%, #ef6c00 100%);
        box-shadow: 0 4px 12px rgba(245, 124, 0, 0.25);
    }
    
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: rgba(255,255,255,0.9);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
    }
    
    /* MUI Typography */
    .mui-title {
        font-size: 24px;
        font-weight: 500;
        color: #212121;
        margin-bottom: 16px;
    }
    
    .mui-section-title {
        font-size: 18px;
        font-weight: 500;
        color: #212121;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* MUI Chip */
    .mui-chip {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .mui-chip.purple {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    
    .mui-chip.green {
        background: #e8f5e9;
        color: #388e3c;
    }
    
    /* MUI Divider */
    .mui-divider {
        height: 1px;
        background: #e0e0e0;
        margin: 20px 0;
    }
    
    /* Pivot Table Styling */
    .pivot-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .pivot-table th {
        background: #1976d2;
        color: white;
        padding: 12px 8px;
        font-weight: 500;
        font-size: 13px;
        text-align: center;
        border: none;
    }
    
    .pivot-table th.purple {
        background: #7b1fa2;
    }
    
    .pivot-table td {
        padding: 10px 8px;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
        font-size: 14px;
        color: #424242;
    }
    
    .pivot-table tr:hover td {
        background: #e3f2fd;
        cursor: pointer;
    }
    
    .pivot-table .total-row td {
        background: #f5f5f5;
        font-weight: 600;
        color: #212121;
    }
    
    /* Vendor Table */
    .vendor-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .vendor-table th {
        background: #388e3c;
        color: white;
        padding: 12px 16px;
        font-weight: 500;
        font-size: 13px;
        text-align: left;
    }
    
    .vendor-table th:last-child {
        text-align: center;
    }
    
    .vendor-table td {
        padding: 10px 16px;
        border-bottom: 1px solid #e0e0e0;
        font-size: 14px;
        color: #424242;
    }
    
    .vendor-table td:last-child {
        text-align: center;
        font-weight: 500;
    }
    
    .vendor-table tr:hover td {
        background: #e8f5e9;
        cursor: pointer;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Text color fix for light theme */
    p, span, label, .stMarkdown {
        color: #212121 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #212121 !important;
    }
    
    /* Selectbox and inputs */
    .stSelectbox label, .stTextInput label {
        color: #424242 !important;
    }
    
    /* Metric native */
    [data-testid="stMetricValue"] {
        color: #212121 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #616161 !important;
    }
</style>
""", unsafe_allow_html=True)

# Google Sheet config
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
    df = pd.read_csv(url, low_memory=False)
    return df

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%B %d, %Y, %H:%M')
    except:
        return pd.NaT

def get_aging_bucket(days):
    if pd.isna(days) or days < 0:
        return None
    elif days == 0:
        return '0'
    elif days == 1:
        return '1'
    elif days == 2:
        return '2'
    elif days == 3:
        return '3'
    elif days == 4:
        return '4'
    elif days == 5:
        return '5'
    elif days <= 7:
        return '6-7'
    elif days <= 10:
        return '8-10'
    elif days <= 15:
        return '11-15'
    elif days <= 20:
        return '16-20'
    elif days <= 25:
        return '21-25'
    elif days <= 30:
        return '26-30'
    else:
        return '30+'

BUCKET_ORDER = ['0', '1', '2', '3', '4', '5', '6-7', '8-10', '11-15', '16-20', '21-25', '26-30', '30+']

# Session state
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'filter_bucket' not in st.session_state:
    st.session_state.filter_bucket = None
if 'filter_zone' not in st.session_state:
    st.session_state.filter_zone = None
if 'filter_vendor' not in st.session_state:
    st.session_state.filter_vendor = None

def go_home():
    st.session_state.view = 'home'
    st.session_state.filter_bucket = None
    st.session_state.filter_zone = None
    st.session_state.filter_vendor = None

def go_to(view):
    st.session_state.view = view

def go_to_aging(zone, bucket):
    st.session_state.view = 'aging_detail'
    st.session_state.filter_zone = zone
    st.session_state.filter_bucket = bucket

def go_to_vendor(vendor):
    st.session_state.view = 'vendor_detail'
    st.session_state.filter_vendor = vendor

# Load data
try:
    df = load_data()
    
    # Filter data
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    # Calculate aging
    approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
    today = datetime.now()
    approved['aging_days'] = (today - approved['qc_date']).dt.days
    approved['aging_bucket'] = approved['aging_days'].apply(get_aging_bucket)
    
    # Split data
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    
    pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
    pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
    qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
    qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']
    
    display_cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                    'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at',
                    'logistics_partner_handedover_at', 'logistics_partner_name',
                    'QC or zone', 'Order Type', 'aging_days', 'aging_bucket']
    
    if st.session_state.view == 'home':
        # App Bar Header
        st.markdown(f"""
            <div class="mui-appbar">
                <div class="mui-appbar-title">📦 G-Ops Backlog Dashboard</div>
                <div class="mui-appbar-subtitle">Last updated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        with col5:
            if st.button("🔄 REFRESH DATA", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # Summary Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Approved</div>
                    <div class="metric-value">{len(approved):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class="metric-card purple">
                    <div class="metric-label">PK Zone</div>
                    <div class="metric-value">{len(pk_zone):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="metric-card green">
                    <div class="metric-label">QC Center</div>
                    <div class="metric-value">{len(qc_center):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class="metric-card orange">
                    <div class="metric-label">Handover</div>
                    <div class="metric-value">{len(handover):,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Handover Section
        st.markdown("""
            <div class="mui-card">
                <div class="mui-section-title">🚚 Handover to Logistics</div>
                <span class="mui-chip">PK Zone + QC Center Combined</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Handover Orders", f"{len(handover):,}")
        with col2:
            if st.button("VIEW HANDOVER →", key="btn_handover", use_container_width=True):
                go_to('handover')
                st.rerun()
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ==================== AGING PIVOT TABLES ====================
        st.markdown("""
            <div class="mui-card">
                <div class="mui-section-title">📊 Aging Analysis - Normal Orders</div>
                <span class="mui-chip">Click on any count to view orders</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Create aging pivot data
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        # Two columns for pivot tables
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p style="font-weight:500; color:#7b1fa2; margin-bottom:8px;">📍 PK Zone - Normal Orders</p>', unsafe_allow_html=True)
            
            # Create clickable pivot table
            for i, bucket in enumerate(BUCKET_ORDER):
                count = pk_aging[bucket]
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f'<span style="color:#424242;">{bucket} days</span>', unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"pk_aging_{bucket}", use_container_width=True):
                            go_to_aging('PK Zone', bucket)
                            st.rerun()
                    else:
                        st.markdown(f'<span style="color:#9e9e9e;">0</span>', unsafe_allow_html=True)
            
            st.markdown(f'<div style="background:#f5f5f5; padding:8px; border-radius:4px; margin-top:8px;"><strong>Total: {len(pk_normal)}</strong></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p style="font-weight:500; color:#388e3c; margin-bottom:8px;">🏢 QC Center - Normal Orders</p>', unsafe_allow_html=True)
            
            for i, bucket in enumerate(BUCKET_ORDER):
                count = qc_aging[bucket]
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f'<span style="color:#424242;">{bucket} days</span>', unsafe_allow_html=True)
                with c2:
                    if count > 0:
                        if st.button(f"{count}", key=f"qc_aging_{bucket}", use_container_width=True):
                            go_to_aging('PK QC Center', bucket)
                            st.rerun()
                    else:
                        st.markdown(f'<span style="color:#9e9e9e;">0</span>', unsafe_allow_html=True)
            
            st.markdown(f'<div style="background:#f5f5f5; padding:8px; border-radius:4px; margin-top:8px;"><strong>Total: {len(qc_normal)}</strong></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ==================== VENDOR TABLE ====================
        st.markdown("""
            <div class="mui-card">
                <div class="mui-section-title">🏪 PK Zone Vendors - Normal Orders</div>
                <span class="mui-chip green">Click on any vendor to view orders</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Get vendor counts
        vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False)
        
        # Display as clickable list
        col1, col2, col3 = st.columns(3)
        vendors_list = list(vendor_counts.items())
        
        for i, (vendor, count) in enumerate(vendors_list):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(f"{vendor}: {count}", key=f"vendor_{i}", use_container_width=True):
                    go_to_vendor(vendor)
                    st.rerun()
        
        st.markdown(f'<div style="background:#f5f5f5; padding:12px; border-radius:4px; margin-top:16px; text-align:center;"><strong>Total Vendors: {len(vendor_counts)} | Total Orders: {len(pk_normal)}</strong></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ==================== ORIGINAL SECTIONS ====================
        # PK Zone Section
        st.markdown("""
            <div class="mui-card">
                <div class="mui-section-title">📍 PK Zone Orders</div>
                <span class="mui-chip purple">QC Approved - All Order Types</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(pk_normal):,}")
        with col2:
            if st.button("VIEW NORMAL →", key="btn_pk_n", use_container_width=True):
                go_to('pk_n')
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(pk_ai):,}")
        with col4:
            if st.button("VIEW AI →", key="btn_pk_a", use_container_width=True):
                go_to('pk_a')
                st.rerun()
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # QC Center Section
        st.markdown("""
            <div class="mui-card">
                <div class="mui-section-title">🏢 QC Center Orders</div>
                <span class="mui-chip green">QC Approved - All Order Types</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(qc_normal):,}")
        with col2:
            if st.button("VIEW NORMAL →", key="btn_qc_n", use_container_width=True):
                go_to('qc_n')
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(qc_ai):,}")
        with col4:
            if st.button("VIEW AI →", key="btn_qc_a", use_container_width=True):
                go_to('qc_a')
                st.rerun()
    
    elif st.session_state.view == 'aging_detail':
        # Aging Detail View
        zone = st.session_state.filter_zone
        bucket = st.session_state.filter_bucket
        
        if zone == 'PK Zone':
            data = pk_normal[pk_normal['aging_bucket'] == bucket]
            color = "#7b1fa2"
            emoji = "📍"
        else:
            data = qc_normal[qc_normal['aging_bucket'] == bucket]
            color = "#388e3c"
            emoji = "🏢"
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← BACK", use_container_width=True):
                go_home()
                st.rerun()
        with col2:
            st.markdown(f'<div class="mui-title">{emoji} {zone} - {bucket} Days Aging</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="mui-chip">{len(data):,} Normal Orders</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button(
                "⬇️ EXPORT CSV",
                data.to_csv(index=False),
                f"{zone}_{bucket}_days_orders.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Filter data
        filtered = data.copy()
        if search:
            search_lower = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(search_lower, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)
    
    elif st.session_state.view == 'vendor_detail':
        # Vendor Detail View
        vendor = st.session_state.filter_vendor
        data = pk_normal[pk_normal['vendor'] == vendor]
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← BACK", use_container_width=True):
                go_home()
                st.rerun()
        with col2:
            st.markdown(f'<div class="mui-title">🏪 {vendor}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="mui-chip green">{len(data):,} Normal Orders | PK Zone</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button(
                "⬇️ EXPORT CSV",
                data.to_csv(index=False),
                f"{vendor}_orders.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Filter data
        filtered = data.copy()
        if search:
            search_lower = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(search_lower, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)
    
    else:
        # Original Detail Views
        views = {
            'handover': ('🚚 Handover Orders', handover),
            'pk_n': ('📍 PK Zone - Normal Orders', pk_normal),
            'pk_a': ('📍 PK Zone - AI Orders', pk_ai),
            'qc_n': ('🏢 QC Center - Normal Orders', qc_normal),
            'qc_a': ('🏢 QC Center - AI Orders', qc_ai)
        }
        
        title, data = views[st.session_state.view]
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← BACK", use_container_width=True):
                go_home()
                st.rerun()
        with col2:
            st.markdown(f'<div class="mui-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="mui-chip">{len(data):,} orders</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button(
                "⬇️ EXPORT CSV",
                data.to_csv(index=False),
                f"{st.session_state.view}_orders.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Filter data
        filtered = data.copy()
        if search:
            search_lower = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(search_lower, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(search_lower, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
