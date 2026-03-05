"""
ResearchHub AI - Multi-page Streamlit Frontend
Main application entry point with navigation and page routing
"""

import streamlit as st
from pages import home, chat, uploads, discover, summarize, research_assistant, workspace

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="ResearchHub AI",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/researchhub-ai",
        "Report a bug": "https://github.com/yourusername/researchhub-ai/issues",
        "About": "ResearchHub AI - Intelligent Research Companion"
    }
)

# Initialize session state for page
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# ============================================================================
# Custom CSS Styling
# ============================================================================

# ============================================================================
# Custom CSS Styling
# ============================================================================

st.markdown("""
<style>
    /* Cache busting with unique identifier */
    :root {
        --theme-version: v2;
    }
    
    /* Hide Streamlit's default page navigation */
    [data-testid="stSidebarNavLink"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }
    
    /* Main page background */
    .stApp {
        background-color: #1a1a2e !important;
    }
    
    /* Main container */
    .main {
        padding-top: 1rem;
        background-color: #0f3460 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {
        display: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        border: none !important;
        transition: all 0.3s ease;
        background-color: #2980b9 !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        background-color: #3498db !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(41, 128, 185, 0.3);
    }
    
    .stButton > button[kind="secondary"] {
        background-color: #34495e !important;
        color: white !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #2c3e50 !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #34495e !important;
        padding: 10px;
        background-color: #16213e !important;
        color: #ecf0f1 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border: 2px solid #2980b9 !important;
        background-color: #0f3460 !important;
        color: #ecf0f1 !important;
    }
    
    /* Text and headings */
    h1, h2, h3, h4, h5, h6 {
        color: #ecf0f1 !important;
    }
    
    p {
        color: #bdc3c7 !important;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: 0;
        border-top: 2px solid #34495e;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background-color: #16213e !important;
        color: #ecf0f1 !important;
    }
    
    /* Tab styling */
    [data-testid="stTabs"] [aria-selected="true"] {
        border-bottom: 3px solid #2980b9;
        color: #ecf0f1 !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: #16213e !important;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2980b9;
    }
    
    [data-testid="metric-container"] > div:nth-child(1) {
        color: #95a5a6 !important;
    }
    
    [data-testid="metric-container"] > div:nth-child(2) {
        color: #ecf0f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Session State Initialization
# ============================================================================

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'selected_paper' not in st.session_state:
    st.session_state.selected_paper = None

if 'selected_workspace' not in st.session_state:
    st.session_state.selected_workspace = None

# ============================================================================
# Sidebar Navigation
# ============================================================================

with st.sidebar:
    st.markdown("""
        <div style="
            padding: 15px 0;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h2 style="
                color: #2980b9;
                margin: 0;
                font-size: 24px;
                font-weight: 700;
            ">ResearchHub</h2>
            <p style="color: #95a5a6; font-size: 11px; margin: 5px 0 0 0;">
                Research Intelligence Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### Navigation", help="Select a page to navigate")
    
    # Navigation buttons
    nav_pages = {
        "Dashboard": "home",
        "Chat": "chat",
        "Library": "uploads",
        "Discover": "discover",
        "Summarize": "summarize",
        "Research": "research_assistant",
        "Workspace": "workspace"
    }
    
    for page_name in nav_pages.keys():
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary"
        ):
            st.session_state.page = page_name
            st.rerun()
    
    st.divider()
    
    # System information
    st.markdown("### System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Status", "Online")
    
    with col2:
        st.metric("Version", "1.0.0")
    
    st.divider()
    
    # Footer
    st.markdown("""
        <div style="
            text-align: center;
            color: #7f8c8d;
            font-size: 10px;
            margin-top: 20px;
        ">
            <p>Built for Research</p>
            <p>Powered by AI</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# Page Routing
# ============================================================================

if st.session_state.page == "Dashboard":
    home.show()

elif st.session_state.page == "Chat":
    chat.show()

elif st.session_state.page == "Library":
    uploads.show()

elif st.session_state.page == "Discover":
    discover.show()

elif st.session_state.page == "Summarize":
    summarize.show()

elif st.session_state.page == "Research":
    research_assistant.show()

elif st.session_state.page == "Workspace":
    workspace.show()