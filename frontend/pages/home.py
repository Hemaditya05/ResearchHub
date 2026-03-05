"""Home/Dashboard page for ResearchHub AI"""
import streamlit as st
from datetime import datetime
from utils.storage import get_paper_count, get_workspace_count, get_recent_papers

def render_stat_card(label: str, value: str, icon: str = "📊"):
    """Render a statistics card"""
    col = st.container()
    with col:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
                padding: 20px;
                border-radius: 10px;
                color: white;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            ">
                <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">{value}</div>
                <div style="font-size: 14px; opacity: 0.9;">{label}</div>
            </div>
        """, unsafe_allow_html=True)

def render_paper_card(paper: dict):
    """Render a paper card for recent activity"""
    paper_id = paper.get('paper_id', 'Unknown')
    title = paper.get('title', 'Untitled Paper')
    timestamp = paper.get('upload_timestamp', '')
    char_count = paper.get('char_count', 0)
    
    # Format timestamp
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_date = dt.strftime("%b %d, %Y")
        except:
            formatted_date = "Recently"
    else:
        formatted_date = "Recently"
    
    st.markdown(f"""
        <div style="
            background: #16213e;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #2980b9;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            <div style="font-weight: bold; color: #ecf0f1; margin-bottom: 5px;">{title}</div>
            <div style="font-size: 12px; color: #95a5a6;">
                ID: <code style="color: #bdc3c7;">{paper_id}</code> | {formatted_date}
                {f' | {char_count:,} characters' if char_count else ''}
            </div>
        </div>
    """, unsafe_allow_html=True)

def show():
    """Render the home page"""
    
    # Page title
    st.markdown("""
        <h1 style="
            color: #2980b9;
            text-align: center;
            margin-bottom: 30px;
            font-size: 42px;
        ">ResearchHub AI</h1>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
        <div style="
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #2980b9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            <h3 style="margin-top: 0; color: #2980b9;">Welcome to ResearchHub AI</h3>
            <p style="color: #bdc3c7; line-height: 1.6;">
                Your intelligent research platform. Upload papers, discover insights, chat with AI about your research, 
                organize your work in workspaces, and get personalized research assistance.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # System Status Section
    st.markdown("### System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style="
                background: #16213e;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                border: 1px solid #34495e;
            ">
                <div style="font-size: 14px; color: #95a5a6; margin-bottom: 10px;">Backend Status</div>
                <div style="font-size: 18px; font-weight: bold; color: #27ae60;">Online</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        paper_count = get_paper_count()
        st.markdown(f"""
            <div style="
                background: #16213e;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                border: 1px solid #34495e;
            ">
                <div style="font-size: 14px; color: #95a5a6; margin-bottom: 10px;">Papers Uploaded</div>
                <div style="font-size: 18px; font-weight: bold; color: #3498db;">{paper_count}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        workspace_count = get_workspace_count()
        st.markdown(f"""
            <div style="
                background: #16213e;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                border: 1px solid #34495e;
            ">
                <div style="font-size: 14px; color: #95a5a6; margin-bottom: 10px;">Workspaces</div>
                <div style="font-size: 18px; font-weight: bold; color: #e74c3c;">{workspace_count}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style="
                background: #16213e;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                border: 1px solid #34495e;
            ">
                <div style="font-size: 14px; color: #95a5a6; margin-bottom: 10px;">AI Status</div>
                <div style="font-size: 18px; font-weight: bold; color: #f39c12;">Active</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick Actions
    st.markdown("### Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("Upload Paper", use_container_width=True, key="home_upload"):
            st.session_state.page = "Library"
            st.rerun()
    
    with action_col2:
        if st.button("Chat with AI", use_container_width=True, key="home_chat"):
            st.session_state.page = "Chat"
            st.rerun()
    
    with action_col3:
        if st.button("Discover Papers", use_container_width=True, key="home_discover"):
            st.session_state.page = "Discover"
            st.rerun()
    
    with action_col4:
        if st.button("Manage Workspaces", use_container_width=True, key="home_workspace"):
            st.session_state.page = "Workspace"
            st.rerun()
    
    st.divider()
    
    # Recent Activity
    st.markdown("### Recent Activity")
    
    recent_papers = get_recent_papers(limit=5)
    
    if recent_papers:
        st.markdown("#### Recently Uploaded Papers")
        for paper in recent_papers:
            render_paper_card(paper)
    else:
        st.markdown("""
            <div style="
                background: #16213e;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #f39c12;
                color: #ecf0f1;
                margin-bottom: 15px;
            ">
                📄 No papers uploaded yet. Start by uploading your first research paper!
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Features Overview
    st.markdown("### Key Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **Research Library**
        - Upload and organize research papers
        - Persistent paper library
        - Quick access to all uploads
        
        **AI Chat**
        - Chat with AI about your papers
        - Conversational research assistance
        - Full message history
        """)
    
    with feature_col2:
        st.markdown("""
        **Paper Discovery**
        - Search and discover new papers
        - View detailed summaries
        - Save to workspaces
        
        **Workspace Organization**
        - Create multiple research workspaces
        - Organize papers by project
        - Collaborate on research
        """)
    
    st.divider()
    
    # Footer
    st.markdown("""
        <div style="
            text-align: center;
            color: #95a5a6;
            font-size: 12px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        ">
            <p>ResearchHub AI | Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)
