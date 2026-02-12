import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog Dashboard", page_icon="📦", layout="wide")

# Simple Dark Theme
st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    #MainMenu, footer, header { visibility: hidden; }
    h1, h2, h3, h4 { color: #f0f6fc !important; }
    p, span, label { color: #c9d1d9 !important; }
    [data-testid="stMetricValue"] { color: #f0f6fc !important; }
    [data-testid="stMetricLabel"] { color: #8b949e !important; }
</style>
""", unsafe_allow_html=True)

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
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'aging_zone' not in st.session_state:
    st.session_state.aging_zone = None
if 'aging_bucket' not in st.session_state:
    st.session_state.aging_bucket = None
if 'vendor_name' not in st.session_state:
    st.session_state.vendor_name = None

# ============ SIDEBAR - Always visible ============
with st.sidebar:
    st.title("📦 Navigation")
    st.divider()
    
    if st.button("🏠 Home Dashboard", use_container_width=True, key="sidebar_home"):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button("🔄 Refresh Data", use_container_width=True, key="sidebar_refresh"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.caption("Quick Links:")
    
    if st.button("🚚 Handover", use_container_width=True, key="sb_hand"):
        st.session_state.page = 'handover'
        st.rerun()
    if st.button("📍 PK Zone Normal", use_container_width=True, key="sb_pkn"):
        st.session_state.page = 'pk_normal'
        st.rerun()
    if st.button("📍 PK Zone AI", use_container_width=True, key="sb_pka"):
        st.session_state.page = 'pk_ai'
        st.rerun()
    if st.button("🏢 QC Center Normal", use_container_width=True, key="sb_qcn"):
        st.session_state.page = 'qc_normal'
        st.rerun()
    if st.button("🏢 QC Center AI", use_container_width=True, key="sb_qca"):
        st.session_state.page = 'qc_ai'
        st.rerun()

try:
    df = load_data()
    
    # Prepare data
    approved = df[df['latest_status'] == 'QC_APPROVED'].copy()
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    approved['qc_date'] = approved['qc_approved_at'].apply(parse_date)
    approved['aging_days'] = (datetime.now() - approved['qc_date']).dt.days
    approved['aging_bucket'] = approved['aging_days'].apply(get_aging_bucket)
    
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

    # ===================== HOME PAGE =====================
    if st.session_state.page == 'home':
        
        st.title("📦 G-Ops Backlog Dashboard")
        st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
        
        st.divider()
        
        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Approved", f"{len(approved):,}")
        c2.metric("PK Zone", f"{len(pk_zone):,}")
        c3.metric("QC Center", f"{len(qc_center):,}")
        c4.metric("Handover", f"{len(handover):,}")
        
        st.divider()
        
        # ============ HANDOVER SECTION ============
        st.subheader("🚚 Handover to Logistics")
        st.caption("Orders handed over to logistics partner (PK Zone + QC Center)")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Handover Orders", f"{len(handover):,}")
        with col2:
            if st.button("View Handover Orders", key="v_handover"):
                st.session_state.page = 'handover'
                st.rerun()
        
        st.divider()
        
        # ============ PK ZONE SECTION ============
        st.subheader("📍 PK Zone Orders")
        st.caption("QC Approved orders from PK Zone")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(pk_normal):,}")
        with col2:
            if st.button("View PK Normal", key="v_pk_n"):
                st.session_state.page = 'pk_normal'
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(pk_ai):,}")
        with col4:
            if st.button("View PK AI", key="v_pk_a"):
                st.session_state.page = 'pk_ai'
                st.rerun()
        
        st.divider()
        
        # ============ QC CENTER SECTION ============
        st.subheader("🏢 QC Center Orders")
        st.caption("QC Approved orders from QC Center")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(qc_normal):,}")
        with col2:
            if st.button("View QC Normal", key="v_qc_n"):
                st.session_state.page = 'qc_normal'
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(qc_ai):,}")
        with col4:
            if st.button("View QC AI", key="v_qc_a"):
                st.session_state.page = 'qc_ai'
                st.rerun()
        
        st.divider()
        
        # ============ AGING PIVOT TABLES ============
        st.subheader("📊 Aging Analysis - Normal Orders")
        st.caption("Select aging bucket to view orders")
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📍 PK Zone Normal**")
            pk_select = st.selectbox(
                "Select aging to view orders:",
                ['-- Select --'] + [f"{b} days ({pk_aging[b]} orders)" for b in BUCKET_ORDER if pk_aging[b] > 0],
                key="pk_ag"
            )
            if pk_select != '-- Select --':
                st.session_state.page = 'aging'
                st.session_state.aging_zone = 'PK Zone'
                st.session_state.aging_bucket = pk_select.split(' days')[0]
                st.rerun()
            
            st.dataframe(
                pd.DataFrame({'Days': BUCKET_ORDER, 'Count': [pk_aging[b] for b in BUCKET_ORDER]}),
                hide_index=True, use_container_width=True
            )
        
        with col2:
            st.markdown("**🏢 QC Center Normal**")
            qc_select = st.selectbox(
                "Select aging to view orders:",
                ['-- Select --'] + [f"{b} days ({qc_aging[b]} orders)" for b in BUCKET_ORDER if qc_aging[b] > 0],
                key="qc_ag"
            )
            if qc_select != '-- Select --':
                st.session_state.page = 'aging'
                st.session_state.aging_zone = 'PK QC Center'
                st.session_state.aging_bucket = qc_select.split(' days')[0]
                st.rerun()
            
            st.dataframe(
                pd.DataFrame({'Days': BUCKET_ORDER, 'Count': [qc_aging[b] for b in BUCKET_ORDER]}),
                hide_index=True, use_container_width=True
            )
        
        st.divider()
        
        # ============ VENDOR TABLE ============
        st.subheader("🏪 PK Zone Vendors - Normal Orders")
        st.caption("Select vendor to view their orders")
        
        vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        vendor_counts.columns = ['Vendor', 'Orders']
        
        vendor_select = st.selectbox(
            "Select vendor:",
            ['-- Select --'] + [f"{r['Vendor']} ({r['Orders']} orders)" for _, r in vendor_counts.iterrows()],
            key="vend"
        )
        if vendor_select != '-- Select --':
            st.session_state.page = 'vendor'
            st.session_state.vendor_name = vendor_select.rsplit(' (', 1)[0]
            st.rerun()
        
        st.dataframe(vendor_counts, hide_index=True, use_container_width=True, height=300)

    # ===================== DETAIL PAGES =====================
    else:
        # Back button at top
        if st.button("⬅️ Back to Dashboard", key="back_btn", type="primary"):
            st.session_state.page = 'home'
            st.rerun()
        
        st.divider()
        
        # Determine data
        if st.session_state.page == 'handover':
            title = "🚚 Handover Orders"
            data = handover
        elif st.session_state.page == 'pk_normal':
            title = "📍 PK Zone - Normal Orders"
            data = pk_normal
        elif st.session_state.page == 'pk_ai':
            title = "📍 PK Zone - AI Orders"
            data = pk_ai
        elif st.session_state.page == 'qc_normal':
            title = "🏢 QC Center - Normal Orders"
            data = qc_normal
        elif st.session_state.page == 'qc_ai':
            title = "🏢 QC Center - AI Orders"
            data = qc_ai
        elif st.session_state.page == 'aging':
            zone = st.session_state.aging_zone
            bucket = st.session_state.aging_bucket
            title = f"{'📍' if zone == 'PK Zone' else '🏢'} {zone} - {bucket} Days Aging"
            if zone == 'PK Zone':
                data = pk_normal[pk_normal['aging_bucket'] == bucket]
            else:
                data = qc_normal[qc_normal['aging_bucket'] == bucket]
        elif st.session_state.page == 'vendor':
            vendor = st.session_state.vendor_name
            title = f"🏪 {vendor}"
            data = pk_normal[pk_normal['vendor'] == vendor]
        else:
            title = "Orders"
            data = approved
        
        st.title(title)
        st.caption(f"{len(data):,} orders")
        
        st.divider()
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button("⬇️ Export CSV", data.to_csv(index=False), "orders.csv", "text/csv", use_container_width=True)
        
        # Apply filters
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
        
        # Show data
        cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[cols], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error: {str(e)}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
