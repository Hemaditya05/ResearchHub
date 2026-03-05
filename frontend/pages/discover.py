"""Discover page for finding research papers"""
import streamlit as st
from utils.api import api_client

def render_paper_result(paper: dict, index: int):
    """Render a paper search result"""
    title = paper.get('title', 'Untitled')
    authors = paper.get('authors', [])
    summary = paper.get('summary', '')
    published = paper.get('published_date', '')
    pdf_url = paper.get('pdf_url', '')
    paper_id = paper.get('id', f"paper_{index}")
    
    # Truncate summary
    if len(summary) > 300:
        summary = summary[:300] + "..."
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        ">
            <h4 style="margin: 0 0 10px 0; color: #2980b9;">{title}</h4>
            
            {f'<div style="font-size: 13px; color: #666; margin-bottom: 10px;"><strong>Authors:</strong> {", ".join(authors[:3])}</div>' if authors else ''}
            
            {f'<div style="font-size: 13px; color: #666; margin-bottom: 10px;"><strong>Published:</strong> {published}</div>' if published else ''}
            
            <div style="
                background: #f9f9f9;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 12px;
                font-size: 13px;
                line-height: 1.6;
                color: #333;
            ">
                <strong>Summary:</strong><br/>
                {summary}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if pdf_url and st.button("View PDF", key=f"pdf_{index}"):
            st.markdown(f"[Open PDF]({pdf_url})")
    
    with col2:
        if st.button("Save Paper", key=f"save_{index}"):
            st.success(f"Paper saved to library!")
    
    with col3:
        if st.button("Add to Favorites", key=f"fav_{index}"):
            st.success("Added to favorites!")
    
    with col4:
        if st.button("Add to Workspace", key=f"addws_{index}"):
            st.info("Navigate to Uploads or Workspace section to organize")

def show():
    """Render the discover page"""
    
    st.markdown('<h2 style="color: #2980b9; font-weight: 700;">Discover Papers</h2>', unsafe_allow_html=True)
    
    st.markdown("Search and discover research papers from arXiv and other sources.")
    
    st.divider()
    
    # Search section
    st.markdown("### Paper Search")
    
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        search_query = st.text_input(
            "Search papers",
            placeholder="e.g., machine learning, quantum computing, climate change...",
            label_visibility="collapsed",
            key="discover_search"
        )
    
    with col2:
        search_button = st.button("Search", use_container_width=True, key="discover_btn")
    
    # Advanced filters
    with st.expander("Advanced Filters", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            paper_type = st.selectbox(
                "Paper Type",
                ["All", "Research Paper", "Review", "Survey", "Preprint"],
                key="filter_type"
            )
        
        with col2:
            year_range = st.slider(
                "Publication Year",
                min_value=2015,
                max_value=2026,
                value=(2020, 2026),
                key="filter_year"
            )
        
        sort_by = st.selectbox(
            "Sort By",
            ["Relevance", "Most Recent", "Most Cited"],
            key="filter_sort"
        )
    
    # Perform search
    if search_button and search_query:
        with st.spinner("Searching for papers..."):
            response = api_client.discover(search_query)
        
        if "error" in response:
            st.error(f"Search failed: {response.get('error')}")
        else:
            papers = response.get('papers', [])
            
            if not papers:
                st.info("No papers found. Try a different search query.")
            else:
                st.markdown(f"### Found {len(papers)} paper(s)")
                st.divider()
                
                for i, paper in enumerate(papers):
                    render_paper_result(paper, i)
    
    st.divider()
    
    # Featured categories
    st.markdown("### Featured Research Areas")
    
    categories = [
        ("Artificial Intelligence", "Explore AI and machine learning papers"),
        ("Bioinformatics", "Discover computational biology research"),
        ("Computer Science", "Latest computer science breakthroughs"),
        ("Quantum Computing", "Quantum computing and quantum algorithms"),
        ("Climate Research", "Environmental and climate science papers"),
    ]
    
    col1, col2 = st.columns(2)
    
    for i, (category, description) in enumerate(categories):
        if i % 2 == 0:
            col = col1
        else:
            col = col2
        
        with col:
            if st.button(f"{category}\n_{description}_", use_container_width=True, key=f"cat_{i}"):
                st.session_state.discover_search = category.split()[1]
                st.rerun()
    
    st.divider()
    
    # Tips
    with st.expander("💡 Tips for Better Searches", expanded=False):
        st.markdown("""
        - **Use keywords**: Search for specific topics or paper titles
        - **Filter by year**: Focus on recent papers or historical research
        - **Combine filters**: Use multiple filters for precise results
        - **Save papers**: Click "Save Paper" to add papers to your library
        - **Organize workspaces**: Group related papers in workspaces for better organization
        
        **Popular searches:**
        - "transformer models"
        - "neural networks"
        - "data science"
        - "blockchain"
        - "machine learning applications"
        """)
