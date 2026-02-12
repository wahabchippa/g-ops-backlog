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
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    .stApp {
        background-color: #f5f5f5 !important;
        font-family: 'Roboto', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main .block-container {
        background-color: #f5f5f5 !important;
        padding-top: 1rem;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #f5f5f5 !important;
    }
    
    /* MUI App Bar */
    .mui-appbar {
        background: linear-gradient(90deg, #1976d2 0%, #1565c0 100%);
        padding: 20px 24px;
        border-radius: 8px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .mui-appbar-title {
        font-size: 26px;
        font-weight: 500;
        color: #ffffff;
        margin: 0;
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
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 16px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        border-radius: 8px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.25);
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
    
    /* Typography */
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
    }
    
    /* Chip */
    .mui-chip {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .mui-chip.purple { background: #f3e5f5; color: #7b1fa2; }
    .mui-chip.green { background: #e8f5e9; color: #388e3c; }
    
    /* Divider */
    .mui-divider {
        height: 1px;
        background: #e0e0e0;
        margin: 20px 0;
    }
    
    /* Fix text colors */
    p, span, label, .stMarkdown, h1, h2, h3, h4, h5, h6 {
        color: #212121 !important;
    }
    
    [data-testid="stMetricValue"] { color: #212121 !important; }
    [data-testid="stMetricLabel"] { color: #616161 !important; }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #ffffff;
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
    elif days == 0: return '0'
    elif days == 1: return '1'
    elif days == 2: return '2'
    elif days == 3: return '3'
    elif days == 4: return '4'
    elif days == 5: return '5'
    elif days <= 7: return '6-7'
    elif days <= 10: return '8-10'
    elif days <= 15: return '11-15'
    elif days <= 20: return '16-20'
    elif days <= 25: return '21-25'
    elif days <= 30: return '26-30'
    else: return '30+'

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
    
    # ============ HOME VIEW ============
    if st.session_state.view == 'home':
        # App Bar
        st.markdown(f"""
            <div class="mui-appbar">
                <div class="mui-appbar-title">📦 G-Ops Backlog Dashboard</div>
                <div class="mui-appbar-subtitle">Last updated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Refresh
        if st.button("🔄 REFRESH DATA", key="refresh_main"):
            st.cache_data.clear()
            st.rerun()
        
        # Summary Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Total Approved</div><div class="metric-value">{len(approved):,}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card purple"><div class="metric-label">PK Zone</div><div class="metric-value">{len(pk_zone):,}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card green"><div class="metric-label">QC Center</div><div class="metric-value">{len(qc_center):,}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card orange"><div class="metric-label">Handover</div><div class="metric-value">{len(handover):,}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Handover Section
        st.markdown('<div class="mui-card"><div class="mui-section-title">🚚 Handover to Logistics</div><span class="mui-chip">PK Zone + QC Center</span></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Orders", f"{len(handover):,}")
        with col2:
            if st.button("VIEW HANDOVER ORDERS →", key="btn_handover"):
                st.session_state.view = 'handover'
                st.rerun()
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ========== AGING PIVOT TABLES ==========
        st.markdown('<div class="mui-card"><div class="mui-section-title">📊 Aging Analysis - Normal Orders</div><span class="mui-chip">Select aging bucket to view orders</span></div>', unsafe_allow_html=True)
        
        # Create aging data
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📍 PK Zone - Normal Orders**")
            
            # Create DataFrame for aging
            pk_aging_df = pd.DataFrame({
                'Aging (Days)': BUCKET_ORDER,
                'Count': [pk_aging[b] for b in BUCKET_ORDER]
            })
            pk_aging_df['Total'] = len(pk_normal)
            
            # Selectbox for PK Zone aging
            pk_bucket = st.selectbox(
                "Select PK Zone Aging Bucket",
                options=['-- Select --'] + [f"{b} days ({pk_aging[b]} orders)" for b in BUCKET_ORDER if pk_aging[b] > 0],
                key="pk_aging_select"
            )
            
            if pk_bucket != '-- Select --':
                bucket = pk_bucket.split(' days')[0]
                st.session_state.view = 'aging_detail'
                st.session_state.filter_zone = 'PK Zone'
                st.session_state.filter_bucket = bucket
                st.rerun()
            
            # Show counts table
            st.dataframe(pk_aging_df[['Aging (Days)', 'Count']], hide_index=True, use_container_width=True)
            st.markdown(f"**Total: {len(pk_normal)} orders**")
        
        with col2:
            st.markdown("**🏢 QC Center - Normal Orders**")
            
            qc_aging_df = pd.DataFrame({
                'Aging (Days)': BUCKET_ORDER,
                'Count': [qc_aging[b] for b in BUCKET_ORDER]
            })
            
            # Selectbox for QC Center aging
            qc_bucket = st.selectbox(
                "Select QC Center Aging Bucket",
                options=['-- Select --'] + [f"{b} days ({qc_aging[b]} orders)" for b in BUCKET_ORDER if qc_aging[b] > 0],
                key="qc_aging_select"
            )
            
            if qc_bucket != '-- Select --':
                bucket = qc_bucket.split(' days')[0]
                st.session_state.view = 'aging_detail'
                st.session_state.filter_zone = 'PK QC Center'
                st.session_state.filter_bucket = bucket
                st.rerun()
            
            st.dataframe(qc_aging_df[['Aging (Days)', 'Count']], hide_index=True, use_container_width=True)
            st.markdown(f"**Total: {len(qc_normal)} orders**")
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ========== VENDOR TABLE ==========
        st.markdown('<div class="mui-card"><div class="mui-section-title">🏪 PK Zone Vendors - Normal Orders</div><span class="mui-chip green">Select vendor to view orders</span></div>', unsafe_allow_html=True)
        
        vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        vendor_counts.columns = ['Vendor', 'Normal Orders']
        
        # Vendor selectbox
        vendor_options = ['-- Select Vendor --'] + [f"{row['Vendor']} ({row['Normal Orders']} orders)" for _, row in vendor_counts.iterrows()]
        selected_vendor = st.selectbox("Select Vendor", options=vendor_options, key="vendor_select")
        
        if selected_vendor != '-- Select Vendor --':
            vendor_name = selected_vendor.split(' (')[0]
            st.session_state.view = 'vendor_detail'
            st.session_state.filter_vendor = vendor_name
            st.rerun()
        
        # Show vendor table
        st.dataframe(vendor_counts, hide_index=True, use_container_width=True, height=300)
        st.markdown(f"**Total: {len(vendor_counts)} vendors | {len(pk_normal)} orders**")
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ========== PK ZONE SECTION ==========
        st.markdown('<div class="mui-card"><div class="mui-section-title">📍 PK Zone Orders</div><span class="mui-chip purple">QC Approved</span></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal", f"{len(pk_normal):,}")
        with col2:
            if st.button("VIEW NORMAL →", key="btn_pk_n"):
                st.session_state.view = 'pk_n'
                st.rerun()
        with col3:
            st.metric("AI", f"{len(pk_ai):,}")
        with col4:
            if st.button("VIEW AI →", key="btn_pk_a"):
                st.session_state.view = 'pk_a'
                st.rerun()
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # ========== QC CENTER SECTION ==========
        st.markdown('<div class="mui-card"><div class="mui-section-title">🏢 QC Center Orders</div><span class="mui-chip green">QC Approved</span></div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal", f"{len(qc_normal):,}")
        with col2:
            if st.button("VIEW NORMAL →", key="btn_qc_n"):
                st.session_state.view = 'qc_n'
                st.rerun()
        with col3:
            st.metric("AI", f"{len(qc_ai):,}")
        with col4:
            if st.button("VIEW AI →", key="btn_qc_a"):
                st.session_state.view = 'qc_a'
                st.rerun()
    
    # ============ AGING DETAIL VIEW ============
    elif st.session_state.view == 'aging_detail':
        zone = st.session_state.filter_zone
        bucket = st.session_state.filter_bucket
        
        if zone == 'PK Zone':
            data = pk_normal[pk_normal['aging_bucket'] == bucket]
            emoji = "📍"
        else:
            data = qc_normal[qc_normal['aging_bucket'] == bucket]
            emoji = "🏢"
        
        if st.button("← BACK TO DASHBOARD", key="back_aging"):
            st.session_state.view = 'home'
            st.session_state.filter_bucket = None
            st.session_state.filter_zone = None
            st.rerun()
        
        st.markdown(f'<div class="mui-title">{emoji} {zone} - {bucket} Days Aging</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="mui-chip">{len(data):,} Normal Orders</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...", key="search_aging")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries, key="country_aging")
        with col3:
            st.download_button("⬇️ EXPORT CSV", data.to_csv(index=False), f"{zone}_{bucket}_days.csv", "text/csv", use_container_width=True)
        
        filtered = data.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)
    
    # ============ VENDOR DETAIL VIEW ============
    elif st.session_state.view == 'vendor_detail':
        vendor = st.session_state.filter_vendor
        data = pk_normal[pk_normal['vendor'] == vendor]
        
        if st.button("← BACK TO DASHBOARD", key="back_vendor"):
            st.session_state.view = 'home'
            st.session_state.filter_vendor = None
            st.rerun()
        
        st.markdown(f'<div class="mui-title">🏪 {vendor}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="mui-chip green">{len(data):,} Normal Orders | PK Zone</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...", key="search_vendor")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries, key="country_vendor")
        with col3:
            st.download_button("⬇️ EXPORT CSV", data.to_csv(index=False), f"{vendor}_orders.csv", "text/csv", use_container_width=True)
        
        filtered = data.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)
    
    # ============ OTHER DETAIL VIEWS ============
    else:
        views = {
            'handover': ('🚚 Handover Orders', handover),
            'pk_n': ('📍 PK Zone - Normal Orders', pk_normal),
            'pk_a': ('📍 PK Zone - AI Orders', pk_ai),
            'qc_n': ('🏢 QC Center - Normal Orders', qc_normal),
            'qc_a': ('🏢 QC Center - AI Orders', qc_ai)
        }
        
        title, data = views[st.session_state.view]
        
        if st.button("← BACK TO DASHBOARD", key="back_main"):
            st.session_state.view = 'home'
            st.rerun()
        
        st.markdown(f'<div class="mui-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="mui-chip">{len(data):,} orders</span>', unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...", key="search_main")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries, key="country_main")
        with col3:
            st.download_button("⬇️ EXPORT CSV", data.to_csv(index=False), f"{st.session_state.view}_orders.csv", "text/csv", use_container_width=True)
        
        filtered = data.copy()
        if search:
            s = search.lower()
            filtered = filtered[
                filtered['order_number'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['customer_name'].astype(str).str.lower().str.contains(s, na=False) |
                filtered['fleek_id'].astype(str).str.lower().str.contains(s, na=False)
            ]
        if country != 'All':
            filtered = filtered[filtered['customer_country'] == country]
        
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
