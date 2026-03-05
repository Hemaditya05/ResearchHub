"""Workspace management page"""
import streamlit as st
from datetime import datetime
from utils.api import api_client
from utils.storage import (
    load_workspaces, add_workspace, get_workspace,
    load_papers
)

def render_workspace_card(workspace: dict):
    """Render a workspace card"""
    ws_id = workspace.get('workspace_id', 'unknown')
    name = workspace.get('name', 'Untitled Workspace')
    description = workspace.get('description', '')
    created = workspace.get('created_timestamp', '')
    papers_count = len(workspace.get('papers', []))
    
    # Format date
    if created:
        try:
            dt = datetime.fromisoformat(created)
            formatted_date = dt.strftime("%b %d, %Y")
        except:
            formatted_date = "Recently"
    else:
        formatted_date = "Recently"
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        ">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <div>
                    <h4 style="margin: 0; color: #333;">{name}</h4>
                    {f'<div style="font-size: 13px; color: #666; margin-top: 4px;">{description}</div>' if description else ''}
                </div>
                <div style="
                    background: #2980b9;
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                ">
                    {papers_count} papers
                </div>
            </div>
            
            <div style="
                background: #f5f5f5;
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 12px;
                font-family: monospace;
                font-size: 12px;
                color: #666;
            ">
                ID: <strong>{ws_id}</strong>
            </div>
            
            <div style="font-size: 12px; color: #888;">
                Created: {formatted_date}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Open", key=f"open_{ws_id}", use_container_width=True):
            st.session_state.selected_workspace = ws_id
            st.session_state.show_workspace_details = True
    
    with col2:
        if st.button("Add Paper", key=f"addpaper_{ws_id}", use_container_width=True):
            st.session_state.selected_workspace = ws_id
            st.session_state.show_add_paper = True
    
    with col3:
        if st.button("Copy ID", key=f"copy_{ws_id}", use_container_width=True):
            st.success(f"Copied: {ws_id}")
    
    with col4:
        if st.button("Delete", key=f"delete_{ws_id}", use_container_width=True):
            st.warning(f"Workspace deletion not yet implemented")

def show():
    """Render the workspace page"""
    
    st.markdown('<h2 style="color: #2980b9; font-weight: 700;">Workspace Management</h2>', unsafe_allow_html=True)
    
    st.markdown("Create and organize your research papers into workspaces.")
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Create Workspace", "My Workspaces", "Workspace Details"])
    
    # Tab 1: Create Workspace
    with tab1:
        st.markdown("### Create New Workspace")
        
        col1, col2 = st.columns([0.6, 0.4])
        
        with col1:
            ws_name = st.text_input(
                "Workspace Name",
                placeholder="e.g., 'AI Research 2024'",
                key="ws_name_input",
                label_visibility="collapsed"
            )
        
        with col2:
            st.empty()
        
        ws_description = st.text_area(
            "Description (optional)",
            placeholder="Describe the focus of this workspace",
            height=80,
            key="ws_desc_input",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            tags = st.text_input(
                "Tags (comma-separated)",
                placeholder="e.g., AI, machine learning, deep learning",
                key="ws_tags",
                label_visibility="collapsed"
            )
        
        with col2:
            visibility = st.selectbox(
                "Visibility",
                ["Private", "Shared", "Public"],
                key="ws_visibility"
            )
        
        st.divider()
        
        if st.button("Create Workspace", use_container_width=True, key="create_ws_btn"):
            if not ws_name.strip():
                st.warning("Please enter a workspace name!")
            else:
                with st.spinner("Creating workspace..."):
                    response = api_client.create_workspace(ws_name)
                
                if "error" not in response:
                    # Save to local storage
                    workspace_data = {
                        'workspace_id': response.get('id', response.get('workspace_id', f'ws_{datetime.now().timestamp()}')),
                        'name': ws_name,
                        'description': ws_description,
                        'tags': [t.strip() for t in tags.split(',')] if tags else [],
                        'visibility': visibility,
                        'papers': [],
                        'created_timestamp': datetime.now().isoformat()
                    }
                    
                    if add_workspace(workspace_data):
                        st.success(f"Workspace '{ws_name}' created successfully!")
                        st.rerun()
                    else:
                        st.warning("Workspace already exists")
                else:
                    st.error(f"Failed to create workspace: {response.get('error')}")
    
    # Tab 2: My Workspaces
    with tab2:
        st.markdown("### Your Workspaces")
        
        workspaces = load_workspaces()
        
        if not workspaces:
            st.info("Create your first workspace to get started!")
        else:
            # Filter and search
            col1, col2 = st.columns(2)
            
            with col1:
                search_ws = st.text_input(
                    "Search workspaces",
                    placeholder="Search by name or tags...",
                    key="search_ws"
                )
            
            with col2:
                sort_ws = st.selectbox(
                    "Sort by",
                    ["Most Recent", "Name A-Z", "Most Papers"],
                    key="sort_ws"
                )
            
            # Filter workspaces
            filtered_ws = workspaces
            
            if search_ws:
                filtered_ws = [
                    w for w in filtered_ws
                    if search_ws.lower() in w.get('name', '').lower() or
                       any(search_ws.lower() in tag.lower() for tag in w.get('tags', []))
                ]
            
            # Sort workspaces
            if sort_ws == "Most Recent":
                filtered_ws = sorted(
                    filtered_ws,
                    key=lambda w: w.get('created_timestamp', ''),
                    reverse=True
                )
            elif sort_ws == "Name A-Z":
                filtered_ws = sorted(
                    filtered_ws,
                    key=lambda w: w.get('name', '').lower()
                )
            elif sort_ws == "Most Papers":
                filtered_ws = sorted(
                    filtered_ws,
                    key=lambda w: len(w.get('papers', [])),
                    reverse=True
                )
            
            st.markdown(f"**Found {len(filtered_ws)} workspace(s)**")
            
            # Display workspaces
            for workspace in filtered_ws:
                render_workspace_card(workspace)
    
    # Tab 3: Workspace Details
    with tab3:
        st.markdown("### Workspace Details")
        
        workspaces = load_workspaces()
        
        if not workspaces:
            st.info("No workspaces yet. Create one in the 'Create Workspace' tab.")
        else:
            # Select workspace
            ws_options = {w.get('workspace_id'): w.get('name') for w in workspaces}
            
            selected_ws_id = st.selectbox(
                "Select workspace",
                options=list(ws_options.keys()),
                format_func=lambda x: ws_options[x],
                key="detail_ws_select",
                label_visibility="collapsed"
            )
            
            selected_ws = next((w for w in workspaces if w.get('workspace_id') == selected_ws_id), None)
            
            if selected_ws:
                st.divider()
                
                # Workspace info
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Name", selected_ws.get('name', 'N/A'))
                
                with col2:
                    st.metric("Papers", len(selected_ws.get('papers', [])))
                
                with col3:
                    created = selected_ws.get('created_timestamp', '')
                    if created:
                        try:
                            dt = datetime.fromisoformat(created)
                            created_str = dt.strftime("%b %d, %Y")
                        except:
                            created_str = "N/A"
                    else:
                        created_str = "N/A"
                    st.metric("Created", created_str)
                
                with col4:
                    st.metric("Visibility", selected_ws.get('visibility', 'Private'))
                
                st.divider()
                
                # Description
                if selected_ws.get('description'):
                    st.markdown(f"**Description:** {selected_ws.get('description')}")
                
                # Tags
                if selected_ws.get('tags'):
                    st.markdown("**Tags:**")
                    for tag in selected_ws.get('tags', []):
                        st.write(f"• {tag}")
                
                st.divider()
                
                # Papers in workspace
                st.markdown("### Papers in This Workspace")
                
                papers_in_ws = selected_ws.get('papers', [])
                
                if not papers_in_ws:
                    st.info("No papers in this workspace yet.")
                else:
                    st.markdown(f"**{len(papers_in_ws)} paper(s)**")
                    for paper_id in papers_in_ws:
                        st.write(f"• {paper_id}")
                
                st.divider()
                
                # Add papers to workspace
                st.markdown("### Add Papers")
                
                all_papers = load_papers()
                available_papers = [p for p in all_papers if p.get('paper_id') not in papers_in_ws]
                
                if not available_papers:
                    st.info("All papers are already in this workspace.")
                else:
                    paper_options = {p.get('paper_id'): p.get('title', 'Untitled') for p in available_papers}
                    
                    selected_papers = st.multiselect(
                        "Select papers to add",
                        options=list(paper_options.keys()),
                        format_func=lambda x: f"{paper_options[x]} (ID: {x})",
                        key="add_papers_select"
                    )
                    
                    if selected_papers and st.button("Add Selected Papers", use_container_width=True, key="add_papers_btn"):
                        with st.spinner("Adding papers..."):
                            for paper_id in selected_papers:
                                response = api_client.add_paper_to_workspace(selected_ws_id, paper_id)
                                
                                if "error" not in response:
                                    selected_ws['papers'].append(paper_id)
                        
                        st.success("Papers added to workspace!")
                        st.rerun()
