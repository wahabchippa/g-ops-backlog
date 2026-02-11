import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="G-Ops Backlog", page_icon="📦", layout="wide")

# Simple Clean CSS
st.markdown("""
<style>
    #MainMenu, footer, header {display: none;}
    .main .block-container {padding: 2rem 3rem; max-width: 1300px;}
    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-weight: 600;
    }
    .stButton > button:hover {background: #1d4ed8;}
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

def main():
    if 'view' not in st.session_state:
        st.session_state.view = 'home'
    
    df = load_data()
    if df.empty:
        st.error("Cannot load data")
        return
    
    # Data Filters
    approved = df[df['latest_status'] == 'QC_APPROVED'] if 'latest_status' in df.columns else pd.DataFrame()
    
    handover = pd.DataFrame()
    if 'latest_status' in df.columns and 'QC or zone' in df.columns:
        handover = df[(df['latest_status'] == 'HANDED_OVER_TO_LOGISTICS_PARTNER') & (df['QC or zone'].isin(['PK Zone', 'PK QC Center']))]
    
    pk_n = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    pk_a = approved[(approved['QC or zone'] == 'PK Zone') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_n = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'Normal Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    qc_a = approved[(approved['QC or zone'] == 'PK QC Center') & (approved['Order Type'] == 'AI Order')] if 'QC or zone' in approved.columns else pd.DataFrame()
    
    # HOME PAGE
    if st.session_state.view == 'home':
        # Title
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title("📦 G-Ops Backlog Dashboard")
            st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
        with col2:
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
        
        st.divider()
        
        # Summary Metrics
        total = len(pk_n) + len(pk_a) + len(qc_n) + len(qc_a)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Approved", f"{total:,}")
        col2.metric("PK Zone", f"{len(pk_n) + len(pk_a):,}")
        col3.metric("QC Center", f"{len(qc_n) + len(qc_a):,}")
        col4.metric("Handover", f"{len(handover):,}")
        
        st.divider()
        
        # HANDOVER SECTION
        st.subheader("🚚 Handover to Logistics")
        st.caption("Orders handed over to logistics partner (PK Zone + QC Center)")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Handover Orders", f"{len(handover):,}")
        with col2:
            if st.button("View Handover Orders", key="h_btn"):
                st.session_state.view = 'handover'
                st.rerun()
        
        st.divider()
        
        # PK ZONE SECTION
        st.subheader("🏭 PK Zone Orders")
        st.caption("Approved orders from Pakistan Zone")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(pk_n):,}")
        with col2:
            if st.button("View Normal", key="pkn_btn"):
                st.session_state.view = 'pk_n'
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(pk_a):,}")
        with col4:
            if st.button("View AI", key="pka_btn"):
                st.session_state.view = 'pk_a'
                st.rerun()
        
        st.divider()
        
        # QC CENTER SECTION
        st.subheader("🏢 QC Center Orders")
        st.caption("Approved orders from QC Center")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Normal Orders", f"{len(qc_n):,}")
        with col2:
            if st.button("View Normal", key="qcn_btn"):
                st.session_state.view = 'qc_n'
                st.rerun()
        with col3:
            st.metric("AI Orders", f"{len(qc_a):,}")
        with col4:
            if st.button("View AI", key="qca_btn"):
                st.session_state.view = 'qc_a'
                st.rerun()
    
    # DETAIL PAGES
    else:
        pages = {
            'handover': (handover, "🚚 Handover Orders"),
            'pk_n': (pk_n, "🏭 PK Zone - Normal Orders"),
            'pk_a': (pk_a, "🏭 PK Zone - AI Orders"),
            'qc_n': (qc_n, "🏢 QC Center - Normal Orders"),
            'qc_a': (qc_a, "🏢 QC Center - AI Orders")
        }
        
        data, title = pages.get(st.session_state.view, (pd.DataFrame(), ""))
        
        # Back Button & Title
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← Back"):
                st.session_state.view = 'home'
                st.rerun()
        
        st.title(title)
        st.caption(f"Total: {len(data):,} orders")
        
        st.divider()
        
        # Filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search", placeholder="Order #, Customer, Fleek ID")
        with col2:
            countries = ['All'] + sorted(data['customer_country'].dropna().unique().tolist()) if 'customer_country' in data.columns else ['All']
            country = st.selectbox("🌍 Country", countries)
        with col3:
            st.write("")
            st.download_button("📥 Export CSV", data.to_csv(index=False), "orders.csv", "text/csv")
        
        # Filter Data
        fdf = data.copy()
        if search:
            mask = fdf.apply(lambda r: any(search.lower() in str(v).lower() for v in r), axis=1)
            fdf = fdf[mask]
        if country != 'All':
            fdf = fdf[fdf['customer_country'] == country]
        
        # Display
        cols = ['order_number', 'fleek_id', 'customer_name', 'customer_country', 'vendor', 'item_name', 
                'total_order_line_amount', 'qc_approved_at', 'logistics_partner_name', 'QC or zone', 'Order Type']
        cols = [c for c in cols if c in fdf.columns]
        
        st.write(f"**Showing {len(fdf):,} orders**")
        st.dataframe(fdf[cols], use_container_width=True, hide_index=True, height=500)

if __name__ == "__main__":
    main()
