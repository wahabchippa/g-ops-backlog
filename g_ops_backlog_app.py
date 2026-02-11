import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="G-Ops Backlog",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Corporate Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu, footer, header {display: none;}
    
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        padding: 2rem 4rem;
        margin: -1rem -1rem 0 -1rem;
    }
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
    }
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .brand-icon {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .brand-text {
        color: #fff;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .brand-sub {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .header-date {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Stats Cards in Header */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
    }
    .stat-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        background: rgba(255,255,255,0.08);
        transform: translateY(-2px);
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .stat-value {
        color: #fff;
        font-size: 2rem;
        font-weight: 800;
    }
    .stat-card.highlight {
        background: linear-gradient(135deg, rgba(59,130,246,0.2) 0%, rgba(139,92,246,0.2) 100%);
        border-color: rgba(59,130,246,0.3);
    }
    
    /* Main Content */
    .content {
        padding: 2.5rem 4rem;
        max-width: 1400px;
        margin: 0 auto;
        background: #f8fafc;
        min-height: calc(100vh - 250px);
    }
    
    /* Section */
    .section {
        margin-bottom: 2rem;
    }
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.25rem;
    }
    .section-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .section-icon.purple { background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); }
    .section-icon.green { background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); }
    .section-icon.blue { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
    
    /* Order Cards */
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.25rem;
    }
    .cards-grid.single {
        grid-template-columns: 1fr;
        max-width: 400px;
    }
    
    .order-card {
        background: #fff;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 6px 16px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .order-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .order-card.green::before { background: linear-gradient(180deg, #22c55e 0%, #16a34a 100%); }
    .order-card.yellow::before { background: linear-gradient(180deg, #eab308 0%, #ca8a04 100%); }
    .order-card.purple::before { background: linear-gradient(180deg, #a855f7 0%, #7c3aed 100%); }
    
    .order-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 12px 32px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }
    
    .card-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 1rem;
    }
    .card-badge.green { background: #dcfce7; color: #166534; }
    .card-badge.yellow { background: #fef9c3; color: #854d0e; }
    .card-badge.purple { background: #f3e8ff; color: #6b21a8; }
    
    .card-badge-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }
    .card-badge.green .card-badge-dot { background: #22c55e; }
    .card-badge.yellow .card-badge-dot { background: #eab308; }
    .card-badge.purple .card-badge-dot { background: #a855f7; }
    
    .card-value {
        font-size: 3rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .card-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1.25rem;
    }
    .card-action {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #3b82f6;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
        padding-top: 1rem;
        border-top: 1px solid #f1f5f9;
    }
    .card-action:hover {
        color: #2563eb;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(59,130,246,0.3);
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(59,130,246,0.4);
    }
    
    /* Detail Page */
    .detail-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.5rem 4rem;
        margin: -1rem -1rem 2rem -1rem;
    }
    .detail-header-content {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    .detail-title {
        color: #fff;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .detail-count {
        background: rgba(255,255,255,0.1);
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .detail-content {
        padding: 0 4rem 2rem 4rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Filters */
    .filters {
        background: #fff;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
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
    st.markdown('<div class="filters">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search", "", placeholder="Order #, Customer, Fleek ID", key=f"s_{title}", label_visibility="collapsed")
    with col2:
        countries = ['All Countries'] + sorted(df['customer_country'].dropna().unique().tolist()) if 'customer_country' in df.columns else ['All Countries']
        country = st.selectbox("Country", countries, key=f"c_{title}", label_visibility="collapsed")
    with col3:
        st.download_button("📥 Export CSV", df.to_csv(index=False), "orders.csv", "text/csv", key=f"e_{title}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    fdf = df.copy()
    if search:
        mask = fdf.apply(lambda r: any(search.lower() in str(v).lower() for v in r), axis=1)
        fdf = fdf[mask]
    if country != 'All Countries':
        fdf = fdf[fdf['customer_country'] == country]
    
    cols = [c for c in get_cols() if c in fdf.columns]
    st.dataframe(fdf[cols] if cols else fdf, use_container_width=True, hide_index=True, height=500)

def main():
    if 'view' not in st.session_state:
        st.session_state.view = 'home'
    
    df = load_data()
    if df.empty:
        st.error("Cannot load data")
        return
    
    approved = df[df['latest_status'] == 'QC_APPROVED'] if 'latest_status' in df.columns else pd.DataFrame()
    
    handover = pd.DataFrame()
    if 'latest_status' in df.columns and 'QC or zone' in df.columns:
        handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    pk_n = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    pk_a = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_n = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_a = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    
    total = len(pk_n) + len(pk_a) + len(qc_n) + len(qc_a)
    
    if st.session_state.view == 'home':
        # HEADER
        st.markdown(f"""
        <div class="header">
            <div class="header-content">
                <div class="header-top">
                    <div class="brand">
                        <div class="brand-icon">📦</div>
                        <div>
                            <div class="brand-text">G-Ops Backlog</div>
                            <div class="brand-sub">Operations Dashboard</div>
                        </div>
                    </div>
                    <div class="header-date">{datetime.now().strftime('%A, %B %d, %Y')}</div>
                </div>
                <div class="stats-grid">
                    <div class="stat-card highlight">
                        <div class="stat-label">Total Approved</div>
                        <div class="stat-value">{total:,}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">PK Zone</div>
                        <div class="stat-value">{len(pk_n) + len(pk_a):,}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">QC Center</div>
                        <div class="stat-value">{len(qc_n) + len(qc_a):,}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Handover</div>
                        <div class="stat-value">{len(handover):,}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        col1, col2, col3 = st.columns([5, 1, 1])
        with col3:
            if st.button("🔄 Refresh"):
                st.cache_data.clear()
                st.rerun()
        
        st.markdown('<div class="content">', unsafe_allow_html=True)
        
        # HANDOVER SECTION
        st.markdown("""
        <div class="section">
            <div class="section-title">
                <span class="section-icon purple">🚚</span>
                Handover to Logistics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div class="order-card purple">
                <span class="card-badge purple"><span class="card-badge-dot"></span> Handed Over</span>
                <div class="card-value">{len(handover):,}</div>
                <div class="card-label">Orders handed over to logistics partner</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Handover Orders", key="h"):
                st.session_state.view = 'handover'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PK ZONE SECTION
        st.markdown("""
        <div class="section">
            <div class="section-title">
                <span class="section-icon green">🏭</span>
                PK Zone Orders
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="order-card green">
                <span class="card-badge green"><span class="card-badge-dot"></span> Normal Orders</span>
                <div class="card-value">{len(pk_n):,}</div>
                <div class="card-label">Ready for processing</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="pkn"):
                st.session_state.view = 'pk_n'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card yellow">
                <span class="card-badge yellow"><span class="card-badge-dot"></span> AI Orders</span>
                <div class="card-value">{len(pk_a):,}</div>
                <div class="card-label">AI processed orders</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="pka"):
                st.session_state.view = 'pk_a'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # QC CENTER SECTION
        st.markdown("""
        <div class="section">
            <div class="section-title">
                <span class="section-icon blue">🏢</span>
                QC Center Orders
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="order-card green">
                <span class="card-badge green"><span class="card-badge-dot"></span> Normal Orders</span>
                <div class="card-value">{len(qc_n):,}</div>
                <div class="card-label">Ready for processing</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="qcn"):
                st.session_state.view = 'qc_n'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card yellow">
                <span class="card-badge yellow"><span class="card-badge-dot"></span> AI Orders</span>
                <div class="card-value">{len(qc_a):,}</div>
                <div class="card-label">AI processed orders</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Orders", key="qca"):
                st.session_state.view = 'qc_a'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        pages = {
            'handover': (handover, "Handover Orders", len(handover)),
            'pk_n': (pk_n, "PK Zone - Normal Orders", len(pk_n)),
            'pk_a': (pk_a, "PK Zone - AI Orders", len(pk_a)),
            'qc_n': (qc_n, "QC Center - Normal Orders", len(qc_n)),
            'qc_a': (qc_a, "QC Center - AI Orders", len(qc_a))
        }
        
        data, title, count = pages.get(st.session_state.view, (pd.DataFrame(), "", 0))
        
        st.markdown(f"""
        <div class="detail-header">
            <div class="detail-header-content">
                <div class="detail-title">{title}</div>
                <div class="detail-count">{count:,} orders</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 8])
        with col1:
            if st.button("← Back"):
                st.session_state.view = 'home'
                st.rerun()
        
        st.markdown('<div class="detail-content">', unsafe_allow_html=True)
        show_orders(data, title)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
