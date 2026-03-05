"""Summarize page for generating paper summaries"""
import streamlit as st
from utils.api import api_client
from utils.storage import load_papers

def show():
    """Render the summarize page"""
    
    st.markdown('<h2 style="color: #2980b9; font-weight: 700;">Summarize Paper</h2>', unsafe_allow_html=True)
    
    st.markdown("Generate intelligent summaries of your research papers using AI.")
    
    st.divider()
    
    # Paper selection
    st.markdown("### Select Paper to Summarize")
    
    papers = load_papers()
    
    if not papers:
        st.info("Upload some papers first in the Uploads section!")
    else:
        # Create paper options
        paper_options = {p.get('paper_id'): p.get('title', 'Untitled') for p in papers}
        
        # Check if a paper was pre-selected from another page
        default_paper = None
        if st.session_state.get('selected_paper') and st.session_state.get('selected_paper') in paper_options:
            default_paper = st.session_state.get('selected_paper')
        
        selected_paper_id = st.selectbox(
            "Choose a paper",
            options=list(paper_options.keys()),
            format_func=lambda x: f"{paper_options[x]} (ID: {x})",
            index=list(paper_options.keys()).index(default_paper) if default_paper else 0,
            key="summarize_select",
            label_visibility="collapsed"
        )
        
        # Display selected paper info
        selected_paper = next((p for p in papers if p.get('paper_id') == selected_paper_id), None)
        if selected_paper:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Title", selected_paper.get('title', 'N/A')[:30] + "...")
            
            with col2:
                st.metric("Characters", f"{selected_paper.get('char_count', 0):,}")
            
            with col3:
                from datetime import datetime
                upload_date = selected_paper.get('upload_timestamp', '')
                if upload_date:
                    try:
                        dt = datetime.fromisoformat(upload_date)
                        formatted = dt.strftime("%b %d, %Y")
                    except:
                        formatted = "N/A"
                else:
                    formatted = "N/A"
                st.metric("Uploaded", formatted)
        
        st.divider()
        
        # Summary options
        st.markdown("### Summary Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            summary_length = st.radio(
                "Summary Length",
                ["Short (2-3 paragraphs)", "Medium (5-7 paragraphs)", "Long (10+ paragraphs)"],
                key="summary_length"
            )
        
        with col2:
            summary_focus = st.multiselect(
                "Focus Areas",
                ["Key Findings", "Methodology", "Conclusions", "Related Work", "Future Directions"],
                default=["Key Findings", "Methodology", "Conclusions"],
                key="summary_focus"
            )
        
        st.divider()
        
        # Generate button
        if st.button("Generate Summary", use_container_width=True, key="generate_summary_btn"):
            with st.spinner("Generating summary..."):
                response = api_client.summarize(selected_paper_id)
            
            if "error" in response:
                st.error(f"Failed to generate summary: {response.get('error')}")
            else:
                summary_text = response.get('summary', response.get('response', 'No summary generated'))
                
                # Display summary
                st.markdown("### Summary")
                
                st.markdown(f"""
                    <div style="
                        background: #ecf0f1;
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 4px solid #2980b9;
                        line-height: 1.8;
                    ">
                        {summary_text}
                    </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                # Export options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Copy to Clipboard", key="copy_summary"):
                        st.success("Summary copied!")
                
                with col2:
                    st.download_button(
                        label="Download as Text",
                        data=summary_text,
                        file_name=f"summary_{selected_paper_id}.txt",
                        mime="text/plain",
                        key="download_summary"
                    )
                
                with col3:
                    if st.button("Ask Follow-up", key="followup_summary"):
                        st.session_state.page = "Chat"
                        st.rerun()
                
                st.divider()
                
                # Related actions
                st.markdown("### What's Next?")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Add to Workspace", use_container_width=True, key="addws_summary"):
                        st.info("Navigate to Uploads or Workspace to organize this paper")
                
                with col2:
                    if st.button("🔍 Find Related Papers", use_container_width=True, key="related_summary"):
                        st.session_state.page = "Discover"
                        st.rerun()
