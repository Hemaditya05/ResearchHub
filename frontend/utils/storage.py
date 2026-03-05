"""Data storage and persistence utilities"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

DATA_DIR = "data"
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
CHATS_FILE = os.path.join(DATA_DIR, "chats.json")
WORKSPACES_FILE = os.path.join(DATA_DIR, "workspaces.json")

def ensure_data_dir():
    """Ensure data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_papers() -> List[Dict[str, Any]]:
    """Load papers from persistent storage"""
    ensure_data_dir()
    if os.path.exists(PAPERS_FILE):
        try:
            with open(PAPERS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load papers: {e}")
            return []
    return []

def save_papers(papers: List[Dict[str, Any]]):
    """Save papers to persistent storage"""
    ensure_data_dir()
    try:
        with open(PAPERS_FILE, 'w') as f:
            json.dump(papers, f, indent=2, default=str)
    except Exception as e:
        st.error(f"Could not save papers: {e}")

def add_paper(paper_data: Dict[str, Any]) -> bool:
    """Add a new paper to storage"""
    papers = load_papers()
    
    # Check if paper already exists
    if any(p.get('paper_id') == paper_data.get('paper_id') for p in papers):
        return False
    
    # Add upload timestamp if not present
    if 'upload_timestamp' not in paper_data:
        paper_data['upload_timestamp'] = datetime.now().isoformat()
    
    papers.append(paper_data)
    save_papers(papers)
    return True

def get_paper(paper_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific paper by ID"""
    papers = load_papers()
    return next((p for p in papers if p.get('paper_id') == paper_id), None)

def delete_paper(paper_id: str) -> bool:
    """Delete a paper from storage"""
    papers = load_papers()
    original_count = len(papers)
    papers = [p for p in papers if p.get('paper_id') != paper_id]
    
    if len(papers) < original_count:
        save_papers(papers)
        return True
    return False

def load_workspaces() -> List[Dict[str, Any]]:
    """Load workspaces from persistent storage"""
    ensure_data_dir()
    if os.path.exists(WORKSPACES_FILE):
        try:
            with open(WORKSPACES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load workspaces: {e}")
            return []
    return []

def save_workspaces(workspaces: List[Dict[str, Any]]):
    """Save workspaces to persistent storage"""
    ensure_data_dir()
    try:
        with open(WORKSPACES_FILE, 'w') as f:
            json.dump(workspaces, f, indent=2, default=str)
    except Exception as e:
        st.error(f"Could not save workspaces: {e}")

def add_workspace(workspace_data: Dict[str, Any]) -> bool:
    """Add a new workspace to storage"""
    workspaces = load_workspaces()
    
    if any(w.get('workspace_id') == workspace_data.get('workspace_id') for w in workspaces):
        return False
    
    if 'created_timestamp' not in workspace_data:
        workspace_data['created_timestamp'] = datetime.now().isoformat()
    
    workspaces.append(workspace_data)
    save_workspaces(workspaces)
    return True

def get_workspace(workspace_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific workspace by ID"""
    workspaces = load_workspaces()
    return next((w for w in workspaces if w.get('workspace_id') == workspace_id), None)

def load_chat_history(session_key: str = "default") -> List[Dict[str, str]]:
    """Load chat history from persistent storage"""
    ensure_data_dir()
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, 'r') as f:
                chats = json.load(f)
                return chats.get(session_key, [])
        except Exception as e:
            st.warning(f"Could not load chat history: {e}")
            return []
    return []

def save_chat_history(messages: List[Dict[str, str]], session_key: str = "default"):
    """Save chat history to persistent storage"""
    ensure_data_dir()
    try:
        chats = {}
        if os.path.exists(CHATS_FILE):
            with open(CHATS_FILE, 'r') as f:
                chats = json.load(f)
        
        chats[session_key] = messages
        with open(CHATS_FILE, 'w') as f:
            json.dump(chats, f, indent=2, default=str)
    except Exception as e:
        st.error(f"Could not save chat history: {e}")

def add_chat_message(role: str, content: str, session_key: str = "default"):
    """Add a message to chat history"""
    messages = load_chat_history(session_key)
    messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    save_chat_history(messages, session_key)
    return messages

def get_recent_papers(limit: int = 5) -> List[Dict[str, Any]]:
    """Get recently uploaded papers"""
    papers = load_papers()
    return sorted(
        papers,
        key=lambda p: p.get('upload_timestamp', ''),
        reverse=True
    )[:limit]

def get_paper_count() -> int:
    """Get total number of uploaded papers"""
    return len(load_papers())

def get_workspace_count() -> int:
    """Get total number of workspaces"""
    return len(load_workspaces())
