import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="G-Ops Backlog Dashboard",
    page_icon="📦",
    layout="wide"
)

# Minimal Dark Theme - NO button styling
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
    }
    
    .main .block-container {
        background-color: #0d1117;
        padding-top: 2rem;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1, h2, h3 {
        color: #f0f6fc !important;
    }
    
    p, span, label {
        color: #c9d1d9 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #f0f6fc !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
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

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_zone' not in st.session_state:
    st.session_state.selected_zone = None
if 'selected_bucket' not in st.session_state:
    st.session_state.selected_bucket = None
if 'selected_vendor' not in st.session_state:
    st.session_state.selected_vendor = None

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

    # ============ SIDEBAR NAVIGATION ============
    with st.sidebar:
        st.title("📦 Navigation")
        
        if st.button("🏠 Home Dashboard", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
        
        st.divider()
        st.subheader("Quick Links")
        
        if st.button(f"🚚 Handover ({len(handover)})", use_container_width=True):
            st.session_state.current_page = 'handover'
            st.rerun()
        
        if st.button(f"📍 PK Zone Normal ({len(pk_normal)})", use_container_width=True):
            st.session_state.current_page = 'pk_n'
            st.rerun()
            
        if st.button(f"📍 PK Zone AI ({len(pk_ai)})", use_container_width=True):
            st.session_state.current_page = 'pk_a'
            st.rerun()
            
        if st.button(f"🏢 QC Center Normal ({len(qc_normal)})", use_container_width=True):
            st.session_state.current_page = 'qc_n'
            st.rerun()
            
        if st.button(f"🏢 QC Center AI ({len(qc_ai)})", use_container_width=True):
            st.session_state.current_page = 'qc_a'
            st.rerun()
        
        st.divider()
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # ============ MAIN CONTENT ============
    if st.session_state.current_page == 'home':
        st.title("📦 G-Ops Backlog Dashboard")
        st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
        
        st.divider()
        
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Approved", f"{len(approved):,}")
        col2.metric("PK Zone", f"{len(pk_zone):,}")
        col3.metric("QC Center", f"{len(qc_center):,}")
        col4.metric("Handover", f"{len(handover):,}")
        
        st.divider()
        
        # ========== AGING PIVOT TABLES ==========
        st.subheader("📊 Aging Analysis - Normal Orders")
        
        pk_aging = pk_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        qc_aging = qc_normal.groupby('aging_bucket').size().reindex(BUCKET_ORDER, fill_value=0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📍 PK Zone - Normal Orders**")
            
            # Aging dropdown
            pk_options = ['-- Select Aging --'] + [f"{b} days ({pk_aging[b]})" for b in BUCKET_ORDER if pk_aging[b] > 0]
            pk_selected = st.selectbox("Select to view orders:", pk_options, key="pk_aging_dd")
            
            if pk_selected != '-- Select Aging --':
                bucket = pk_selected.split(' days')[0]
                st.session_state.current_page = 'aging_detail'
                st.session_state.selected_zone = 'PK Zone'
                st.session_state.selected_bucket = bucket
                st.rerun()
            
            # Show table
            aging_df = pd.DataFrame({'Days': BUCKET_ORDER, 'Count': [pk_aging[b] for b in BUCKET_ORDER]})
            st.dataframe(aging_df, hide_index=True, use_container_width=True)
            st.caption(f"Total: {len(pk_normal)} orders")
        
        with col2:
            st.markdown("**🏢 QC Center - Normal Orders**")
            
            qc_options = ['-- Select Aging --'] + [f"{b} days ({qc_aging[b]})" for b in BUCKET_ORDER if qc_aging[b] > 0]
            qc_selected = st.selectbox("Select to view orders:", qc_options, key="qc_aging_dd")
            
            if qc_selected != '-- Select Aging --':
                bucket = qc_selected.split(' days')[0]
                st.session_state.current_page = 'aging_detail'
                st.session_state.selected_zone = 'PK QC Center'
                st.session_state.selected_bucket = bucket
                st.rerun()
            
            aging_df2 = pd.DataFrame({'Days': BUCKET_ORDER, 'Count': [qc_aging[b] for b in BUCKET_ORDER]})
            st.dataframe(aging_df2, hide_index=True, use_container_width=True)
            st.caption(f"Total: {len(qc_normal)} orders")
        
        st.divider()
        
        # ========== VENDOR TABLE ==========
        st.subheader("🏪 PK Zone Vendors - Normal Orders")
        
        vendor_counts = pk_normal.groupby('vendor').size().sort_values(ascending=False).reset_index()
        vendor_counts.columns = ['Vendor', 'Orders']
        
        vendor_list = ['-- Select Vendor --'] + [f"{r['Vendor']} ({r['Orders']})" for _, r in vendor_counts.iterrows()]
        vendor_selected = st.selectbox("Select vendor to view orders:", vendor_list, key="vendor_dd")
        
        if vendor_selected != '-- Select Vendor --':
            vendor_name = vendor_selected.rsplit(' (', 1)[0]
            st.session_state.current_page = 'vendor_detail'
            st.session_state.selected_vendor = vendor_name
            st.rerun()
        
        st.dataframe(vendor_counts, hide_index=True, use_container_width=True, height=300)
        st.caption(f"{len(vendor_counts)} vendors | {len(pk_normal)} orders")
    
    # ============ AGING DETAIL PAGE ============
    elif st.session_state.current_page == 'aging_detail':
        zone = st.session_state.selected_zone
        bucket = st.session_state.selected_bucket
        
        if zone == 'PK Zone':
            data = pk_normal[pk_normal['aging_bucket'] == bucket]
        else:
            data = qc_normal[qc_normal['aging_bucket'] == bucket]
        
        st.title(f"{'📍' if zone == 'PK Zone' else '🏢'} {zone} - {bucket} Days")
        st.caption(f"{len(data):,} Normal Orders")
        
        st.divider()
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button("⬇️ Export", data.to_csv(index=False), f"{zone}_{bucket}.csv", "text/csv", use_container_width=True)
        
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
        
        cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[cols], use_container_width=True, height=500)
    
    # ============ VENDOR DETAIL PAGE ============
    elif st.session_state.current_page == 'vendor_detail':
        vendor = st.session_state.selected_vendor
        data = pk_normal[pk_normal['vendor'] == vendor]
        
        st.title(f"🏪 {vendor}")
        st.caption(f"{len(data):,} Normal Orders | PK Zone")
        
        st.divider()
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button("⬇️ Export", data.to_csv(index=False), f"{vendor}.csv", "text/csv", use_container_width=True)
        
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
        
        cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[cols], use_container_width=True, height=500)
    
    # ============ OTHER PAGES ============
    else:
        pages = {
            'handover': ('🚚 Handover Orders', handover),
            'pk_n': ('📍 PK Zone - Normal', pk_normal),
            'pk_a': ('📍 PK Zone - AI', pk_ai),
            'qc_n': ('🏢 QC Center - Normal', qc_normal),
            'qc_a': ('🏢 QC Center - AI', qc_ai)
        }
        
        title, data = pages.get(st.session_state.current_page, ('Orders', approved))
        
        st.title(title)
        st.caption(f"{len(data):,} orders")
        
        st.divider()
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID...")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.download_button("⬇️ Export", data.to_csv(index=False), "orders.csv", "text/csv", use_container_width=True)
        
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
        
        cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[cols], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error: {str(e)}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
