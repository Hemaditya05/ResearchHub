"""Chat page with conversational AI interface"""
import streamlit as st
from utils.api import api_client
from utils.storage import load_chat_history, save_chat_history, add_chat_message

def render_message(role: str, content: str):
    """Render a chat message as a bubble"""
    if role == "user":
        st.markdown(f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 10px;
            ">
                <div style="
                    background: #2980b9;
                    color: white;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 70%;
                    word-wrap: break-word;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:  # assistant
        st.markdown(f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                margin-bottom: 10px;
            ">
                <div style="
                    background: #ecf0f1;
                    color: #2c3e50;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 70%;
                    word-wrap: break-word;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                ">
                    {content}
                </div>
            </div>
        """, unsafe_allow_html=True)

def show():
    """Render the chat page"""
    
    st.markdown("""
        <h2 style="color: #2c3e50;">Chat with AI</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("Discuss your research papers with our intelligent AI assistant.")
    
    st.divider()
    
    # Initialize session state for chat
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = load_chat_history("main")
    
    # Chat container with scrollable area
    st.markdown("### Conversation")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_messages:
            st.info("👋 Start a conversation by asking a question about your research!")
        else:
            for message in st.session_state.chat_messages:
                render_message(message['role'], message['content'])
    
    st.divider()
    
    # Input area
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        user_input = st.text_input(
            "Your message",
            label_visibility="collapsed",
            placeholder="Ask me anything about your research...",
            key="chat_input"
        )
    
    with col2:
        send_button = st.button("Send", key="chat_send_btn", use_container_width=True)
    
    # Process user message
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        add_chat_message("user", user_input, "main")
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            response = api_client.chat(user_input)
        
        if "error" not in response:
            # Extract assistant message
            assistant_message = response.get('response', response.get('message', 'No response'))
            if isinstance(assistant_message, dict):
                assistant_message = str(assistant_message)
            
            # Add assistant message to history
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": str(assistant_message)
            })
            add_chat_message("assistant", str(assistant_message), "main")
        else:
            error_msg = response.get('error', 'An error occurred')
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"⚠️ Error: {error_msg}"
            })
            add_chat_message("assistant", f"⚠️ Error: {error_msg}", "main")
        
        st.rerun()
    
    st.divider()
    
    # Chat controls
    col1, col2, col3 = st.columns([0.33, 0.33, 0.34])
    
    with col1:
        if st.button("Clear Chat", use_container_width=True, key="clear_chat"):
            st.session_state.chat_messages = []
            save_chat_history([], "main")
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("Export Chat", use_container_width=True, key="export_chat"):
            import json
            chat_json = json.dumps(st.session_state.chat_messages, indent=2)
            st.download_button(
                label="Download as JSON",
                data=chat_json,
                file_name="chat_history.json",
                mime="application/json",
                key="download_chat"
            )
    
    with col3:
        st.markdown("---")
    
    # Chat tips
    with st.expander("Tips for Better Chats", expanded=False):
        st.markdown("""
        - Ask questions about specific papers
        - Request summaries or explanations
        - Get research recommendations
        - Ask about research trends
        - Get help organizing your research
        
        **Example questions:**
        - "Summarize the key findings from my uploaded papers"
        - "What are the latest trends in AI research?"
        - "Help me organize papers by topic"
        """)
