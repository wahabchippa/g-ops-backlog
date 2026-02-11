import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="G-Ops Backlog Tool",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
    }
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 100%;
        background: linear-gradient(135deg, rgba(59,130,246,0.2) 0%, rgba(147,51,234,0.2) 100%);
        border-radius: 0 20px 20px 0;
    }
    .dashboard-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    .dashboard-header p {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    .header-stats {
        display: flex;
        gap: 3rem;
        margin-top: 1.5rem;
        position: relative;
        z-index: 1;
    }
    .header-stat {
        text-align: left;
    }
    .header-stat-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .header-stat-label {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section Container */
    .section-box {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 0.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .section-title-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .section-title-icon.green {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    }
    .section-title-icon.blue {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    }
    .section-title-icon.purple {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
    }
    .section-subtitle {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0 0 1.5rem 0;
        padding-left: 52px;
    }
    
    /* Order Card */
    .order-card {
        background: #f8fafc;
        border-radius: 14px;
        padding: 1.75rem;
        border: 2px solid #e2e8f0;
        transition: all 0.25s ease;
        cursor: pointer;
    }
    .order-card:hover {
        border-color: #cbd5e1;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }
    .order-card.green {
        border-left: 4px solid #22c55e;
    }
    .order-card.green:hover {
        background: linear-gradient(135deg, #f0fdf4 0%, #f8fafc 100%);
        border-color: #86efac;
    }
    .order-card.yellow {
        border-left: 4px solid #eab308;
    }
    .order-card.yellow:hover {
        background: linear-gradient(135deg, #fefce8 0%, #f8fafc 100%);
        border-color: #fde047;
    }
    .order-card.purple {
        border-left: 4px solid #a855f7;
    }
    .order-card.purple:hover {
        background: linear-gradient(135deg, #faf5ff 0%, #f8fafc 100%);
        border-color: #c084fc;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .card-type {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
    }
    .card-type.green {
        background: #dcfce7;
        color: #166534;
    }
    .card-type.yellow {
        background: #fef9c3;
        color: #854d0e;
    }
    .card-type.purple {
        background: #f3e8ff;
        color: #6b21a8;
    }
    
    .card-value {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .card-value.green { color: #16a34a; }
    .card-value.yellow { color: #ca8a04; }
    .card-value.purple { color: #9333ea; }
    
    .card-label {
        font-size: 0.95rem;
        color: #475569;
        font-weight: 500;
    }
    
    .card-action {
        margin-top: 1.25rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.875rem;
        color: #3b82f6;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton > button:hover {
        background: #2563eb;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
    }
    
    /* Page Header */
    .page-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .page-header h2 {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    .page-header p {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
    }
    
    .refresh-time {
        text-align: right;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: -1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_dump_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_display_columns():
    return ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
            'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at',
            'logistics_partner_handedover_at', 'logistics_partner_name',
            'product_brand', 'QC or zone', 'Order Type']

def display_orders_page(df, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No orders found.")
        return
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("Search by Order #, Customer, Fleek ID", "", key=f"search_{title}")
    with col2:
        if 'customer_country' in df.columns:
            countries = ['All Countries'] + sorted(df['customer_country'].dropna().unique().tolist())
            country = st.selectbox("Country", countries, key=f"country_{title}")
        else:
            country = "All Countries"
    with col3:
        st.write("")
        st.write("")
        csv = df.to_csv(index=False)
        st.download_button("Export CSV", csv, f"orders.csv", "text/csv", key=f"csv_{title}")
    
    filtered_df = df.copy()
    if search:
        search = search.lower()
        mask = filtered_df.apply(lambda row: any(search in str(val).lower() for val in row), axis=1)
        filtered_df = filtered_df[mask]
    
    if country != "All Countries" and 'customer_country' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['customer_country'] == country]
    
    display_cols = get_display_columns()
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    st.markdown(f"**{len(filtered_df):,} orders found**")
    
    if not filtered_df.empty:
        display_df = filtered_df[available_cols].copy() if available_cols else filtered_df.copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)

def main():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    
    df = load_dump_data()
    
    if df.empty:
        st.error("Unable to load data.")
        return
    
    # QC APPROVED Orders
    approved_df = df[df['latest_status'] == 'QC_APPROVED'].copy() if 'latest_status' in df.columns else pd.DataFrame()
    
    # HANDOVER Orders (PK Zone + QC Center mixed)
    handover_df = pd.DataFrame()
    if 'latest_status' in df.columns and 'QC or zone' in df.columns:
        handover_df = df[
            (df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & 
            (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))
        ].copy()
    
    # PK Zone Orders (Approved)
    pk_zone_normal = pd.DataFrame()
    pk_zone_ai = pd.DataFrame()
    qc_center_normal = pd.DataFrame()
    qc_center_ai = pd.DataFrame()
    
    if 'QC or zone' in approved_df.columns and 'Order Type' in approved_df.columns:
        pk_zone_normal = approved_df[(approved_df['QC or zone'] == 'PK Zone') & (approved_df['Order Type'] == 'Normal Order')]
        pk_zone_ai = approved_df[(approved_df['QC or zone'] == 'PK Zone') & (approved_df['Order Type'] == 'AI Order')]
        qc_center_normal = approved_df[(approved_df['QC or zone'] == 'PK QC Center') & (approved_df['Order Type'] == 'Normal Order')]
        qc_center_ai = approved_df[(approved_df['QC or zone'] == 'PK QC Center') & (approved_df['Order Type'] == 'AI Order')]
    
    # Counts
    pk_normal_count = len(pk_zone_normal)
    pk_ai_count = len(pk_zone_ai)
    qc_normal_count = len(qc_center_normal)
    qc_ai_count = len(qc_center_ai)
    handover_count = len(handover_df)
    total_approved = pk_normal_count + pk_ai_count + qc_normal_count + qc_ai_count
    
    # DASHBOARD VIEW
    if st.session_state.current_view == 'dashboard':
        
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Refresh"):
                st.cache_data.clear()
                st.rerun()
        
        st.markdown(f"""
        <div class="dashboard-header">
            <h1>G-Ops Backlog Dashboard</h1>
            <p>Real-time QC Approved Orders Tracking</p>
            <div class="header-stats">
                <div class="header-stat">
                    <div class="header-stat-value">{total_approved:,}</div>
                    <div class="header-stat-label">Approved Orders</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value">{pk_normal_count + pk_ai_count:,}</div>
                    <div class="header-stat-label">PK Zone</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value">{qc_normal_count + qc_ai_count:,}</div>
                    <div class="header-stat-label">QC Center</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value">{handover_count:,}</div>
                    <div class="header-stat-label">Handover</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        now = datetime.now().strftime('%d %b %Y, %H:%M')
        st.markdown(f'<div class="refresh-time">Last updated: {now}</div>', unsafe_allow_html=True)
        
        # ========== HANDOVER SECTION ==========
        st.markdown("""
        <div class="section-box">
            <div class="section-title">
                <span class="section-title-icon purple">🚚</span>
                Handover to Logistics
            </div>
            <p class="section-subtitle">Orders handed over to logistics partner (PK Zone + QC Center)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="order-card purple">
            <div class="card-header">
                <span class="card-type purple">All Handover Orders</span>
            </div>
            <div class="card-value purple">{handover_count:,}</div>
            <div class="card-label">Orders handed over to logistics partner</div>
            <div class="card-action">View all orders →</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Handover Orders", key="handover_btn"):
            st.session_state.current_view = 'handover'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== PK ZONE SECTION ==========
        st.markdown("""
        <div class="section-box">
            <div class="section-title">
                <span class="section-title-icon green">🏭</span>
                PK Zone Orders
            </div>
            <p class="section-subtitle">Approved orders from Pakistan Zone warehouse</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="order-card green">
                <div class="card-header">
                    <span class="card-type green">Normal Orders</span>
                </div>
                <div class="card-value green">{pk_normal_count:,}</div>
                <div class="card-label">Approved orders ready for processing</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Normal Orders", key="pk_normal"):
                st.session_state.current_view = 'pk_zone_normal'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card yellow">
                <div class="card-header">
                    <span class="card-type yellow">AI Orders</span>
                </div>
                <div class="card-value yellow">{pk_ai_count:,}</div>
                <div class="card-label">AI processed orders ready</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open AI Orders", key="pk_ai"):
                st.session_state.current_view = 'pk_zone_ai'
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== QC CENTER SECTION ==========
        st.markdown("""
        <div class="section-box">
            <div class="section-title">
                <span class="section-title-icon blue">🏢</span>
                QC Center Orders
            </div>
            <p class="section-subtitle">Approved orders from Quality Control Center</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="order-card green">
                <div class="card-header">
                    <span class="card-type green">Normal Orders</span>
                </div>
                <div class="card-value green">{qc_normal_count:,}</div>
                <div class="card-label">Approved orders ready for processing</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Normal Orders", key="qc_normal"):
                st.session_state.current_view = 'qc_center_normal'
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="order-card yellow">
                <div class="card-header">
                    <span class="card-type yellow">AI Orders</span>
                </div>
                <div class="card-value yellow">{qc_ai_count:,}</div>
                <div class="card-label">AI processed orders ready</div>
                <div class="card-action">View all orders →</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open AI Orders", key="qc_ai"):
                st.session_state.current_view = 'qc_center_ai'
                st.rerun()
    
    # Detail Pages
    elif st.session_state.current_view == 'handover':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(handover_df, "Handover to Logistics", f"{handover_count:,} orders handed over (PK Zone + QC Center)")
    
    elif st.session_state.current_view == 'pk_zone_normal':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_normal, "PK Zone - Normal Orders", f"{pk_normal_count:,} approved normal orders")
    
    elif st.session_state.current_view == 'pk_zone_ai':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_ai, "PK Zone - AI Orders", f"{pk_ai_count:,} approved AI orders")
    
    elif st.session_state.current_view == 'qc_center_normal':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_normal, "QC Center - Normal Orders", f"{qc_normal_count:,} approved normal orders")
    
    elif st.session_state.current_view == 'qc_center_ai':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_ai, "QC Center - AI Orders", f"{qc_ai_count:,} approved AI orders")

if __name__ == "__main__":
    main()
