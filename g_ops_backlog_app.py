import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="G-Ops Backlog Dashboard",
    page_icon="📦",
    layout="wide"
)

# MUI-style CSS
st.markdown("""
<style>
    /* Import Roboto font (MUI default) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* MUI Card style */
    .mui-card {
        background: #1e1e1e;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2), 0 4px 8px rgba(0,0,0,0.15);
        margin-bottom: 16px;
        transition: box-shadow 0.3s ease;
    }
    
    .mui-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* MUI Metric Card */
    .metric-card {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(25, 118, 210, 0.4);
    }
    
    .metric-card.secondary {
        background: linear-gradient(135deg, #7b1fa2 0%, #6a1b9a 100%);
        box-shadow: 0 4px 12px rgba(123, 31, 162, 0.3);
    }
    
    .metric-card.secondary:hover {
        box-shadow: 0 8px 24px rgba(123, 31, 162, 0.4);
    }
    
    .metric-card.success {
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%);
        box-shadow: 0 4px 12px rgba(56, 142, 60, 0.3);
    }
    
    .metric-card.success:hover {
        box-shadow: 0 8px 24px rgba(56, 142, 60, 0.4);
    }
    
    .metric-card.warning {
        background: linear-gradient(135deg, #f57c00 0%, #ef6c00 100%);
        box-shadow: 0 4px 12px rgba(245, 124, 0, 0.3);
    }
    
    .metric-card.warning:hover {
        box-shadow: 0 8px 24px rgba(245, 124, 0, 0.4);
    }
    
    .metric-label {
        font-size: 14px;
        font-weight: 500;
        color: rgba(255,255,255,0.9);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* MUI Typography */
    .mui-title {
        font-size: 28px;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .mui-subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.6);
        margin-bottom: 24px;
    }
    
    .mui-section-title {
        font-size: 20px;
        font-weight: 500;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* MUI Chip */
    .mui-chip {
        display: inline-block;
        background: rgba(25, 118, 210, 0.15);
        color: #90caf9;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
    }
    
    /* MUI Divider */
    .mui-divider {
        height: 1px;
        background: rgba(255,255,255,0.12);
        margin: 24px 0;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transform: translateY(-1px);
    }
    
    /* Section card */
    .section-card {
        background: #1e1e1e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border-left: 4px solid #1976d2;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .section-card.purple {
        border-left-color: #7b1fa2;
    }
    
    .section-card.green {
        border-left-color: #388e3c;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* App bar style header */
    .app-bar {
        background: #1976d2;
        padding: 16px 24px;
        border-radius: 0 0 12px 12px;
        margin: -1rem -1rem 24px -1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .app-bar-title {
        font-size: 24px;
        font-weight: 500;
        color: #ffffff;
        margin: 0;
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

# Session state
if 'view' not in st.session_state:
    st.session_state.view = 'home'

def go_home():
    st.session_state.view = 'home'

def go_to(view):
    st.session_state.view = view

# Load data
try:
    df = load_data()
    
    # Filter data
    approved = df[df['latest_status'] == 'QC_APPROVED']
    handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
                  (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    pk_zone = approved[approved['QC or zone'] == 'PK Zone']
    qc_center = approved[approved['QC or zone'] == 'PK QC Center']
    
    pk_normal = pk_zone[pk_zone['Order Type'] == 'Normal Order']
    pk_ai = pk_zone[pk_zone['Order Type'] == 'AI Order']
    qc_normal = qc_center[qc_center['Order Type'] == 'Normal Order']
    qc_ai = qc_center[qc_center['Order Type'] == 'AI Order']
    
    display_cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
                    'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at',
                    'logistics_partner_handedover_at', 'logistics_partner_name',
                    'QC or zone', 'Order Type']
    
    if st.session_state.view == 'home':
        # Header
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
                <div class="mui-title">📦 G-Ops Backlog Dashboard</div>
                <div class="mui-subtitle">Last updated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🔄 REFRESH", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # Summary Metrics
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
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
                <div class="metric-card secondary">
                    <div class="metric-label">PK Zone</div>
                    <div class="metric-value">{len(pk_zone):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class="metric-card success">
                    <div class="metric-label">QC Center</div>
                    <div class="metric-value">{len(qc_center):,}</div>
                </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class="metric-card warning">
                    <div class="metric-label">Handover</div>
                    <div class="metric-value">{len(handover):,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        
        # Handover Section
        st.markdown("""
            <div class="section-card">
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
        
        # PK Zone Section
        st.markdown("""
            <div class="section-card purple">
                <div class="mui-section-title">📍 PK Zone Orders</div>
                <span class="mui-chip">QC Approved</span>
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
            <div class="section-card green">
                <div class="mui-section-title">🏢 QC Center Orders</div>
                <span class="mui-chip">QC Approved</span>
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
    
    else:
        # Detail Views
        views = {
            'handover': ('🚚 Handover Orders', handover),
            'pk_n': ('📍 PK Zone - Normal Orders', pk_normal),
            'pk_a': ('📍 PK Zone - AI Orders', pk_ai),
            'qc_n': ('🏢 QC Center - Normal Orders', qc_normal),
            'qc_a': ('🏢 QC Center - AI Orders', qc_ai)
        }
        
        title, data = views[st.session_state.view]
        
        # Back button and title
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
        
        # Display
        st.markdown('<div class="mui-divider"></div>', unsafe_allow_html=True)
        available_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[available_cols], use_container_width=True, height=500)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    if st.button("🔄 Retry"):
        st.cache_data.clear()
        st.rerun()
