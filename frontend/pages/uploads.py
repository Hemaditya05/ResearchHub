"""Uploads page with persistent paper library"""
import streamlit as st
from datetime import datetime
from utils.api import api_client
from utils.storage import (
    load_papers, add_paper, get_paper, delete_paper,
    load_workspaces
)

def render_paper_card(paper: dict):
    """Render a detailed paper card with actions"""
    paper_id = paper.get('paper_id', 'Unknown')
    title = paper.get('title', 'Untitled Paper')
    upload_date = paper.get('upload_timestamp', '')
    char_count = paper.get('char_count', 0)
    
    # Format date
    if upload_date:
        try:
            dt = datetime.fromisoformat(upload_date)
            formatted_date = dt.strftime("%B %d, %Y • %H:%M")
        except:
            formatted_date = "Unknown date"
    else:
        formatted_date = "Recently"
    
    st.markdown(f"""
        <div style="
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #34495e;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 12px;
            ">
                <div>
                    <h4 style="margin: 0; color: #ecf0f1;">{title}</h4>
                    <div style="font-size: 12px; color: #95a5a6; margin-top: 4px;">
                        {formatted_date}
                    </div>
                </div>
            </div>
            
            <div style="
                background: #0f3460;
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 12px;
                font-family: monospace;
                font-size: 12px;
                color: #bdc3c7;
                word-break: break-all;
                border: 1px solid #34495e;
            ">
                Paper ID: <strong style="color: #2980b9;">{paper_id}</strong>
            </div>
            
            {f'<div style="font-size: 12px; color: #95a5a6; margin-bottom: 12px;">Characters: {char_count:,}</div>' if char_count else ''}
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons in columns
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("Chat", key=f"chat_{paper_id}", use_container_width=True):
            st.success(f"Opening chat about paper {paper_id}")
            st.session_state.selected_paper = paper_id
            st.session_state.page = "Chat"
            st.rerun()
    
    with action_col2:
        if st.button("Summarize", key=f"summarize_{paper_id}", use_container_width=True):
            st.session_state.selected_paper = paper_id
            st.session_state.page = "Summarize"
            st.rerun()
    
    with action_col3:
        if st.button("Add to Workspace", key=f"addws_{paper_id}", use_container_width=True):
            st.session_state.selected_paper = paper_id
            st.session_state.show_add_to_workspace = True
    
    with action_col4:
        if st.button("Copy ID", key=f"copy_{paper_id}", use_container_width=True):
            st.success(f"Copied: {paper_id}")

def show():
    """Render the uploads page"""
    
    st.markdown("""
        <h2 style="color: #2980b9;">Research Library</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("Upload, organize, and manage your research papers in one place.")
    
    st.divider()
    
    # Upload section
    st.markdown("### Upload New Paper")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        label_visibility="collapsed",
        key="paper_uploader"
    )
    
    if uploaded_file is not None:
        if st.button("Upload Paper", use_container_width=True, key="upload_btn"):
            with st.spinner("Uploading paper..."):
                response = api_client.upload_paper(uploaded_file)
            
            if "error" not in response:
                # Extract paper metadata
                paper_data = {
                    'paper_id': response.get('id', response.get('paper_id', 'unknown')),
                    'title': response.get('title', uploaded_file.name),
                    'filename': uploaded_file.name,
                    'char_count': response.get('char_count', len(uploaded_file.getvalue())),
                    'upload_timestamp': datetime.now().isoformat(),
                    'status': 'uploaded'
                }
                
                # Save to persistent storage
                if add_paper(paper_data):
                    st.success(f"✅ Paper uploaded successfully! ID: {paper_data['paper_id']}")
                    st.rerun()
                else:
                    st.warning("Paper already exists in library")
            else:
                st.error(f"Upload failed: {response.get('error', 'Unknown error')}")
    
    st.divider()
    
    # Papers library
    st.markdown("### Your Papers")
    
    papers = load_papers()
    
    if not papers:
        st.markdown("""
            <div style="
                background: #16213e;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #f39c12;
                color: #ecf0f1;
                margin-bottom: 15px;
            ">
                👉 Start by uploading your first research paper!
            </div>
        """, unsafe_allow_html=True)
    else:
        # Filter and sort options
        col1, col2 = st.columns(2)
        
        with col1:
            sort_option = st.selectbox(
                "Sort by",
                ["Most Recent", "Oldest First", "Alphabetical"],
                key="sort_papers"
            )
        
        with col2:
            search_term = st.text_input(
                "Search papers",
                placeholder="Search by title or ID...",
                key="search_papers"
            )
        
        # Apply filtering and sorting
        filtered_papers = papers
        
        if search_term:
            filtered_papers = [
                p for p in filtered_papers
                if search_term.lower() in p.get('title', '').lower() or
                   search_term.lower() in p.get('paper_id', '').lower()
            ]
        
        if sort_option == "Most Recent":
            filtered_papers = sorted(
                filtered_papers,
                key=lambda p: p.get('upload_timestamp', ''),
                reverse=True
            )
        elif sort_option == "Oldest First":
            filtered_papers = sorted(
                filtered_papers,
                key=lambda p: p.get('upload_timestamp', '')
            )
        elif sort_option == "Alphabetical":
            filtered_papers = sorted(
                filtered_papers,
                key=lambda p: p.get('title', '').lower()
            )
        
        st.markdown(f"**Found {len(filtered_papers)} paper(s)**")
        
        # Display papers
        for i, paper in enumerate(filtered_papers):
            with st.container():
                render_paper_card(paper)
                
                # Add to workspace modal
                if st.session_state.get('show_add_to_workspace') and st.session_state.get('selected_paper') == paper.get('paper_id'):
                    with st.expander("Add to Workspace", expanded=True):
                        workspaces = load_workspaces()
                        
                        if not workspaces:
                            st.markdown("""
                                <div style="
                                    background: #16213e;
                                    padding: 12px;
                                    border-radius: 6px;
                                    border-left: 4px solid #2980b9;
                                    color: #ecf0f1;
                                    margin-bottom: 10px;
                                ">
                                    No workspaces yet. Create one in the Workspace section.
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            workspace_names = {w.get('workspace_id'): w.get('name') for w in workspaces}
                            selected_ws = st.selectbox(
                                "Select workspace",
                                options=list(workspace_names.keys()),
                                format_func=lambda x: workspace_names[x],
                                key=f"ws_select_{paper.get('paper_id')}"
                            )
                            
                            if st.button("Add to Workspace", key=f"confirm_add_{paper.get('paper_id')}"):
                                with st.spinner("Adding paper to workspace..."):
                                    response = api_client.add_paper_to_workspace(
                                        selected_ws,
                                        paper.get('paper_id')
                                    )
                                
                                if "error" not in response:
                                    st.success("Paper added to workspace!")
                                    st.session_state.show_add_to_workspace = False
                                    st.rerun()
                                else:
                                    st.error(f"Failed to add paper: {response.get('error')}")
    
    st.divider()
    
    # Statistics
    st.markdown("### 📊 Library Statistics")
    
    if papers:
        total_papers = len(papers)
        total_chars = sum(p.get('char_count', 0) for p in papers)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div style="
                    background: #16213e;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    border-top: 3px solid #3498db;
                ">
                    <div style="font-size: 12px; color: #95a5a6; margin-bottom: 8px;">Total Papers</div>
                    <div style="font-size: 24px; font-weight: bold; color: #3498db;">{total_papers}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="
                    background: #16213e;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    border-top: 3px solid #27ae60;
                ">
                    <div style="font-size: 12px; color: #95a5a6; margin-bottom: 8px;">Total Characters</div>
                    <div style="font-size: 24px; font-weight: bold; color: #27ae60;">{total_chars:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_size = total_chars // total_papers if total_papers > 0 else 0
            st.markdown(f"""
                <div style="
                    background: #16213e;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                    border-top: 3px solid #e74c3c;
                ">
                    <div style="font-size: 12px; color: #95a5a6; margin-bottom: 8px;">Avg Paper Size</div>
                    <div style="font-size: 24px; font-weight: bold; color: #e74c3c;">{avg_size:,}</div>
                </div>
            """, unsafe_allow_html=True)
