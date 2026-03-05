"""Research Assistant page for getting research insights"""
import streamlit as st
from utils.api import api_client

def show():
    """Render the research assistant page"""
    
    st.markdown('<h2 style="color: #2980b9; font-weight: 700;">Research Assistant</h2>', unsafe_allow_html=True)
    
    st.markdown("Get personalized research insights, suggestions, and analysis on any topic.")
    
    st.divider()
    
    # Input section
    st.markdown("### Enter Your Research Topic")
    
    topic = st.text_area(
        "Research Topic",
        placeholder="e.g., 'Machine Learning applications in healthcare' or 'Quantum computing breakthroughs'",
        height=100,
        label_visibility="collapsed",
        key="research_topic"
    )
    
    # Research options
    st.markdown("### Analysis Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        research_depth = st.radio(
            "Analysis Depth",
            ["Quick Overview", "Detailed Analysis", "Comprehensive Research"],
            key="research_depth"
        )
    
    with col2:
        include_options = st.multiselect(
            "Include in Analysis",
            ["Literature Review", "Research Gaps", "Innovation Ideas", "Future Directions", "Key Questions"],
            default=["Research Gaps", "Innovation Ideas", "Future Directions"],
            key="research_options"
        )
    
    st.divider()
    
    # Get research assistance
    if st.button("Get Research Assistance", use_container_width=True, key="assist_btn"):
        if not topic.strip():
            st.warning("Please enter a research topic first!")
        else:
            with st.spinner("Analyzing research topic..."):
                response = api_client.assist(topic)
            
            if "error" in response:
                st.error(f"Analysis failed: {response.get('error')}")
            else:
                assistant_response = response.get('response', response.get('assistance', 'No response'))
                
                # Display structured output
                st.markdown("### Research Analysis")
                
                # Parse response if it's structured
                if isinstance(assistant_response, dict):
                    # Display each section
                    if 'summary' in assistant_response:
                        st.markdown("#### Summary")
                        st.info(assistant_response['summary'])
                    
                    if 'gaps' in assistant_response:
                        st.markdown("#### Research Gaps")
                        for gap in assistant_response['gaps']:
                            st.write(f"• {gap}")
                    
                    if 'ideas' in assistant_response:
                        st.markdown("#### Innovation Ideas")
                        for idea in assistant_response['ideas']:
                            st.write(f"• {idea}")
                    
                    if 'innovations' in assistant_response:
                        st.markdown("#### Innovation Suggestions")
                        for innovation in assistant_response['innovations']:
                            st.write(f"• {innovation}")
                else:
                    # Display as formatted text
                    st.markdown(f"""
                        <div style="
                            background: #ecf0f1;
                            padding: 20px;
                            border-radius: 10px;
                            border-left: 4px solid #2980b9;
                            line-height: 1.8;
                        ">
                            {assistant_response}
                        </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                # Export and share options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 Copy Analysis", key="copy_analysis"):
                        st.success("Analysis copied to clipboard!")
                
                with col2:
                    analysis_text = str(assistant_response)
                    st.download_button(
                        label="📥 Download Report",
                        data=analysis_text,
                        file_name=f"research_analysis_{topic[:30]}.txt",
                        mime="text/plain",
                        key="download_analysis"
                    )
                
                with col3:
                    if st.button("🔍 Discover Related Papers", key="discover_from_assist"):
                        st.session_state.discover_search = topic
                        st.session_state.page = "Discover"
                        st.rerun()
                
                st.divider()
                
                # Follow-up actions
                st.markdown("### 📌 Next Steps")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💬 Chat About This", use_container_width=True, key="chat_assist"):
                        st.session_state.chat_topic = topic
                        st.session_state.page = "Chat"
                        st.rerun()
                
                with col2:
                    if st.button("📁 Create Workspace", use_container_width=True, key="create_ws_assist"):
                        st.session_state.new_workspace_topic = topic
                        st.session_state.page = "Workspace"
                        st.rerun()
                
                with col3:
                    if st.button("🎯 New Analysis", use_container_width=True, key="new_analysis"):
                        st.rerun()
    
    st.divider()
    
    # Example topics
    st.markdown("### 💡 Example Research Topics")
    
    examples = [
        ("Machine Learning in Healthcare", "🏥"),
        ("Quantum Computing", "⚛️"),
        ("Climate Change Mitigation", "🌍"),
        ("Blockchain Applications", "⛓️"),
        ("Gene Editing Technologies", "🧬"),
        ("Renewable Energy", "⚡"),
    ]
    
    cols = st.columns(3)
    for i, (example, emoji) in enumerate(examples):
        with cols[i % 3]:
            if st.button(f"{emoji} {example}", use_container_width=True, key=f"example_{i}"):
                st.session_state.research_topic = example
                st.rerun()
    
    st.divider()
    
    # Tips
    with st.expander("💡 How to Get Better Research Insights", expanded=False):
        st.markdown("""
        **Tips for effective research analysis:**
        
        1. **Be specific**: The more specific your topic, the better the analysis
           - ❌ Bad: "AI"
           - ✅ Good: "Applications of transformers in medical imaging"
        
        2. **Include context**: Mention the field and your interests
           - Example: "Sustainable agriculture techniques in developing countries"
        
        3. **Request specific aspects**: Choose relevant analysis options
           - Use "Research Gaps" to find unexplored areas
           - Use "Innovation Ideas" for novel approaches
           - Use "Future Directions" for emerging trends
        
        4. **Follow up with chat**: Use the Chat section to dive deeper into topics
        
        5. **Organize in workspaces**: Save related papers and analyses together
        
        **Best practices:**
        - Research multiple related topics to build comprehensive knowledge
        - Compare different research areas to find interdisciplinary opportunities
        - Keep track of analysis results for future reference
        - Share insights with collaborators
        """)
