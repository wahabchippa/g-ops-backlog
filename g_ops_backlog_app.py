import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="G-Ops Backlog Tool",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main page styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    .main-header p {
        color: #b8d4e8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Dashboard cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #2d5a87;
        transition: transform 0.2s;
        cursor: pointer;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    .metric-card h3 {
        color: #1e3a5f;
        font-size: 0.9rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card .value {
        color: #2d5a87;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .metric-card .subtitle {
        color: #666;
        font-size: 0.8rem;
    }
    
    /* Zone cards */
    .zone-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .zone-card.pk-zone {
        border-left: 4px solid #28a745;
    }
    .zone-card.qc-center {
        border-left: 4px solid #17a2b8;
    }
    .zone-card.ai-zone {
        border-left: 4px solid #ffc107;
    }
    .zone-card.ai-qc {
        border-left: 4px solid #dc3545;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2d5a87 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: white !important;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] label {
        color: #b8d4e8 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2d5a87 0%, #1e3a5f 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Back button */
    .back-btn {
        background: #6c757d;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Google Sheet ID
SHEET_ID = "1GKIgyPTsxNctFL_oUJ9jqqvIjFBTsFi2mOj5VpHCv3o"

@st.cache_data(ttl=300)
def load_dump_data():
    """Load data from Dump tab"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Dump"
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_approved_orders(df):
    """Get only QC_APPROVED orders"""
    if 'latest_status' not in df.columns:
        return pd.DataFrame()
    return df[df['latest_status'] == 'QC_APPROVED'].copy()

def get_display_columns():
    """Get columns to display in tables"""
    return ['order_number', 'fleek_id', 'customer_name', 'customer_country', 
            'vendor', 'item_name', 'total_order_line_amount', 'qc_approved_at', 
            'product_brand', 'QC or zone', 'Order Type']

def display_orders_page(df, title, subtitle, search_term=""):
    """Display orders in a professional table format"""
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
        <h2 style="color: white; margin: 0;">{title}</h2>
        <p style="color: #b8d4e8; margin: 0.5rem 0 0 0;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No orders found.")
        return
    
    # Search filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search by Order #, Customer, Fleek ID", search_term, key=f"search_{title}")
    with col2:
        if 'customer_country' in df.columns:
            countries = ['All Countries'] + sorted(df['customer_country'].dropna().unique().tolist())
            country = st.selectbox("🌍 Country", countries, key=f"country_{title}")
        else:
            country = "All Countries"
    with col3:
        st.write("")
        st.write("")
        csv = df.to_csv(index=False)
        st.download_button("📥 Export CSV", csv, f"{title.lower().replace(' ', '_')}.csv", "text/csv")
    
    # Apply filters
    filtered_df = df.copy()
    if search:
        search = search.lower()
        mask = filtered_df.apply(lambda row: any(search in str(val).lower() for val in row), axis=1)
        filtered_df = filtered_df[mask]
    
    if country != "All Countries" and 'customer_country' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['customer_country'] == country]
    
    # Get display columns
    display_cols = get_display_columns()
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    # Stats row
    st.markdown(f"**📊 Showing {len(filtered_df):,} orders**")
    
    # Display table
    if not filtered_df.empty:
        display_df = filtered_df[available_cols].copy() if available_cols else filtered_df.copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    else:
        st.warning("No orders match your filters.")

def main():
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'dashboard'
    
    # Load data
    df = load_dump_data()
    
    if df.empty:
        st.error("Unable to load data. Please check connection.")
        return
    
    # Get approved orders only
    approved_df = get_approved_orders(df)
    
    # Calculate counts
    pk_zone_approved = approved_df[approved_df['QC or zone'] == 'PK Zone'] if 'QC or zone' in approved_df.columns else pd.DataFrame()
    qc_center_approved = approved_df[approved_df['QC or zone'] == 'PK QC Center'] if 'QC or zone' in approved_df.columns else pd.DataFrame()
    
    # AI Orders (Approved only)
    ai_orders = approved_df[approved_df['Order Type'] == 'AI Order'] if 'Order Type' in approved_df.columns else pd.DataFrame()
    ai_pk_zone = ai_orders[ai_orders['QC or zone'] == 'PK Zone'] if not ai_orders.empty and 'QC or zone' in ai_orders.columns else pd.DataFrame()
    ai_qc_center = ai_orders[ai_orders['QC or zone'] == 'PK QC Center'] if not ai_orders.empty and 'QC or zone' in ai_orders.columns else pd.DataFrame()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: white; font-size: 1.5rem; margin: 0;">📦 G-Ops Backlog</h1>
            <p style="color: #b8d4e8; font-size: 0.8rem;">Operations Management Tool</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 📋 Navigation")
        
        # Navigation buttons
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🏭 Approved Orders")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🟢 PK Zone\n({len(pk_zone_approved):,})", use_container_width=True):
                st.session_state.current_view = 'pk_zone'
                st.rerun()
        with col2:
            if st.button(f"🔵 QC Center\n({len(qc_center_approved):,})", use_container_width=True):
                st.session_state.current_view = 'qc_center'
                st.rerun()
        
        st.markdown("---")
        st.markdown("## 🤖 AI Orders (Approved)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🟡 AI Zone\n({len(ai_pk_zone):,})", use_container_width=True):
                st.session_state.current_view = 'ai_pk_zone'
                st.rerun()
        with col2:
            if st.button(f"🔴 AI QC\n({len(ai_qc_center):,})", use_container_width=True):
                st.session_state.current_view = 'ai_qc_center'
                st.rerun()
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #b8d4e8; font-size: 0.7rem;">
                Last Updated<br>
                {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on current view
    if st.session_state.current_view == 'dashboard':
        # Dashboard Header
        st.markdown("""
        <div class="main-header">
            <h1>📦 G-Ops Backlog Dashboard</h1>
            <p>Real-time Operations Tracking & Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary Stats
        st.markdown("### 📊 Approved Orders Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Approved</h3>
                <div class="value">{len(approved_df):,}</div>
                <div class="subtitle">All QC Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #28a745;">
                <h3>🟢 PK Zone</h3>
                <div class="value" style="color: #28a745;">{len(pk_zone_approved):,}</div>
                <div class="subtitle">Zone Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #17a2b8;">
                <h3>🔵 QC Center</h3>
                <div class="value" style="color: #17a2b8;">{len(qc_center_approved):,}</div>
                <div class="subtitle">QC Center Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #ffc107;">
                <h3>🤖 AI Orders</h3>
                <div class="value" style="color: #ffc107;">{len(ai_orders):,}</div>
                <div class="subtitle">AI Approved Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Access Cards
        st.markdown("### 🚀 Quick Access")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏭 Approved Orders by Zone")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="zone-card pk-zone">
                    <h4 style="color: #28a745; margin: 0;">🟢 PK Zone</h4>
                    <p style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0; color: #28a745;">{len(pk_zone_approved):,}</p>
                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Approved Orders</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="zone-card qc-center">
                    <h4 style="color: #17a2b8; margin: 0;">🔵 QC Center</h4>
                    <p style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0; color: #17a2b8;">{len(qc_center_approved):,}</p>
                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Approved Orders</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🤖 AI Orders by Zone")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="zone-card ai-zone">
                    <h4 style="color: #ffc107; margin: 0;">🟡 AI PK Zone</h4>
                    <p style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0; color: #ffc107;">{len(ai_pk_zone):,}</p>
                    <p style="font-size: 0.8rem; color: #666; margin: 0;">AI Zone Orders</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="zone-card ai-qc">
                    <h4 style="color: #dc3545; margin: 0;">🔴 AI QC Center</h4>
                    <p style="font-size: 1.8rem; font-weight: bold; margin: 0.5rem 0; color: #dc3545;">{len(ai_qc_center):,}</p>
                    <p style="font-size: 0.8rem; color: #666; margin: 0;">AI QC Orders</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <p>👈 Use the sidebar to view detailed order lists</p>
            <p style="font-size: 0.8rem;">Click on any filter to see orders with full details</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.current_view == 'pk_zone':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(pk_zone_approved, "🟢 PK Zone Approved Orders", 
                          f"Showing {len(pk_zone_approved):,} approved orders from PK Zone")
    
    elif st.session_state.current_view == 'qc_center':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(qc_center_approved, "🔵 QC Center Approved Orders", 
                          f"Showing {len(qc_center_approved):,} approved orders from QC Center")
    
    elif st.session_state.current_view == 'ai_pk_zone':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(ai_pk_zone, "🟡 AI Orders - PK Zone", 
                          f"Showing {len(ai_pk_zone):,} AI approved orders from PK Zone")
    
    elif st.session_state.current_view == 'ai_qc_center':
        if st.button("← Back to Dashboard"):
            st.session_state.current_view = 'dashboard'
            st.rerun()
        display_orders_page(ai_qc_center, "🔴 AI Orders - QC Center", 
                          f"Showing {len(ai_qc_center):,} AI approved orders from QC Center")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        G-Ops Backlog Tool | Data Source: Google Sheets | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
