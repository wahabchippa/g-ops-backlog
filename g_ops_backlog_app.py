import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="G-Ops Backlog",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean Minimal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    #MainMenu, footer, header {display: none;}
    
    .main .block-container {
        padding: 2rem 4rem;
        max-width: 1200px;
    }
    
    /* Top Bar */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 2rem;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 2rem;
    }
    .logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #111;
    }
    .logo span {
        color: #666;
        font-weight: 400;
    }
    .date-text {
        color: #666;
        font-size: 0.875rem;
    }
    
    /* Stats Row */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 3rem;
    }
    .stat-box {
        flex: 1;
        padding: 1.25rem 1.5rem;
        background: #fafafa;
        border: 1px solid #eaeaea;
        border-radius: 8px;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .stat-value {
        font-size: 1.75rem;
        font-weight: 600;
        color: #111;
    }
    
    /* Section */
    .section {
        margin-bottom: 2.5rem;
    }
    .section-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #eaeaea;
    }
    
    /* Cards Grid */
    .cards-row {
        display: flex;
        gap: 1rem;
    }
    
    /* Card */
    .card {
        flex: 1;
        padding: 1.5rem;
        background: #fff;
        border: 1px solid #eaeaea;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .card:hover {
        border-color: #111;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .card-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #111;
        margin-bottom: 0.75rem;
    }
    .card-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .card-subtitle {
        font-size: 0.8rem;
        color: #999;
    }
    .card-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        font-size: 0.7rem;
        font-weight: 500;
        border-radius: 4px;
        margin-bottom: 0.75rem;
    }
    .badge-green {
        background: #ecfdf5;
        color: #059669;
    }
    .badge-yellow {
        background: #fffbeb;
        color: #d97706;
    }
    .badge-purple {
        background: #f5f3ff;
        color: #7c3aed;
    }
    
    /* Page Header */
    .page-top {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #eaeaea;
    }
    .page-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111;
    }
    .page-count {
        font-size: 0.875rem;
        color: #666;
    }
    
    /* Button */
    .stButton > button {
        background: #111;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.25rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.15s;
    }
    .stButton > button:hover {
        background: #333;
    }
    
    /* Back link */
    .back-link {
        color: #666;
        font-size: 0.875rem;
        cursor: pointer;
        margin-bottom: 1.5rem;
        display: inline-block;
    }
    .back-link:hover {
        color: #111;
    }
    
    /* Table */
    .stDataFrame {
        border: 1px solid #eaeaea;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
        return pd.read_csv(url, low_memory=False)
    except:
        return pd.DataFrame()

def get_cols():
    return ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
            'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at',
            'logistics_partner_handedover_at', 'logistics_partner_name',
            'product_brand', 'QC or zone', 'Order Type']

def show_orders(df, title):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search", "", placeholder="Order #, Customer, Fleek ID", key=f"s_{title}")
    with col2:
        countries = ['All'] + sorted(df['customer_country'].dropna().unique().tolist()) if 'customer_country' in df.columns else ['All']
        country = st.selectbox("Country", countries, key=f"c_{title}")
    with col3:
        st.write("")
        st.download_button("Export CSV", df.to_csv(index=False), "orders.csv", "text/csv", key=f"e_{title}")
    
    fdf = df.copy()
    if search:
        mask = fdf.apply(lambda r: any(search.lower() in str(v).lower() for v in r), axis=1)
        fdf = fdf[mask]
    if country != 'All':
        fdf = fdf[fdf['customer_country'] == country]
    
    cols = [c for c in get_cols() if c in fdf.columns]
    st.write(f"**{len(fdf):,} orders**")
    st.dataframe(fdf[cols] if cols else fdf, use_container_width=True, hide_index=True, height=450)

def main():
    if 'view' not in st.session_state:
        st.session_state.view = 'home'
    
    df = load_data()
    if df.empty:
        st.error("Cannot load data")
        return
    
    # Data
    approved = df[df['latest_status'] == 'QC_APPROVED'] if 'latest_status' in df.columns else pd.DataFrame()
    
    handover = pd.DataFrame()
    if 'latest_status' in df.columns and 'QC or zone' in df.columns:
        handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    pk_n = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    pk_a = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_n = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_a = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    
    # HOME
    if st.session_state.view == 'home':
        # Top Bar
        st.markdown(f"""
        <div class="top-bar">
            <div class="logo">G-Ops <span>Backlog</span></div>
            <div class="date-text">{datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([6,1])
        with col2:
            if st.button("↻ Refresh"):
                st.cache_data.clear()
                st.rerun()
        
        # Stats
        total = len(pk_n) + len(pk_a) + len(qc_n) + len(qc_a)
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">Total Approved</div>
                <div class="stat-value">{total:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">PK Zone</div>
                <div class="stat-value">{len(pk_n) + len(pk_a):,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">QC Center</div>
                <div class="stat-value">{len(qc_n) + len(qc_a):,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Handover</div>
                <div class="stat-value">{len(handover):,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Handover Section
        st.markdown('<div class="section"><div class="section-header">Handover to Logistics</div></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="card" style="max-width: 350px;">
            <span class="card-badge badge-purple">HANDED OVER</span>
            <div class="card-number">{len(handover):,}</div>
            <div class="card-subtitle">PK Zone + QC Center combined</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Handover Orders", key="h"):
            st.session_state.view = 'handover'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PK Zone Section
        st.markdown('<div class="section"><div class="section-header">PK Zone Orders</div></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="card">
                <span class="card-badge badge-green">NORMAL</span>
                <div class="card-number">{len(pk_n):,}</div>
                <div class="card-subtitle">Ready for processing</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="pkn"):
                st.session_state.view = 'pk_n'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <span class="card-badge badge-yellow">AI</span>
                <div class="card-number">{len(pk_a):,}</div>
                <div class="card-subtitle">AI processed orders</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="pka"):
                st.session_state.view = 'pk_a'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # QC Center Section
        st.markdown('<div class="section"><div class="section-header">QC Center Orders</div></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="card">
                <span class="card-badge badge-green">NORMAL</span>
                <div class="card-number">{len(qc_n):,}</div>
                <div class="card-subtitle">Ready for processing</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="qcn"):
                st.session_state.view = 'qc_n'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <span class="card-badge badge-yellow">AI</span>
                <div class="card-number">{len(qc_a):,}</div>
                <div class="card-subtitle">AI processed orders</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="qca"):
                st.session_state.view = 'qc_a'
                st.rerun()
    
    # DETAIL PAGES
    else:
        if st.button("← Back"):
            st.session_state.view = 'home'
            st.rerun()
        
        pages = {
            'handover': (handover, "Handover Orders", len(handover)),
            'pk_n': (pk_n, "PK Zone - Normal", len(pk_n)),
            'pk_a': (pk_a, "PK Zone - AI", len(pk_a)),
            'qc_n': (qc_n, "QC Center - Normal", len(qc_n)),
            'qc_a': (qc_a, "QC Center - AI", len(qc_a))
        }
        
        data, title, count = pages.get(st.session_state.view, (pd.DataFrame(), "", 0))
        
        st.markdown(f"""
        <div class="page-top">
            <div class="page-title">{title}</div>
            <div class="page-count">{count:,} orders</div>
        </div>
        """, unsafe_allow_html=True)
        
        show_orders(data, title)

if __name__ == "__main__":
    main()
