"""API utility functions for ResearchHub AI backend communication"""
import requests
import json
from typing import Any, Dict, Optional
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

class APIClient:
    """Centralized API client for all backend communications"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.timeout = 30
    
    def _handle_response(self, response):
        """Handle API response with error checking"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"error": str(e)}
    
    def chat(self, message: str) -> Dict[str, Any]:
        """Send a chat message to the AI"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"message": message},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Chat failed: {str(e)}"}
    
    def upload_paper(self, file) -> Dict[str, Any]:
        """Upload a research paper"""
        try:
            files = {"file": file}
            response = requests.post(
                f"{self.base_url}/upload",
                files=files,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    def discover(self, query: str) -> Dict[str, Any]:
        """Discover papers based on query"""
        try:
            response = requests.post(
                f"{self.base_url}/discover",
                json={"query": query},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Discovery failed: {str(e)}"}
    
    def summarize(self, paper_id: str) -> Dict[str, Any]:
        """Get summary of a paper"""
        try:
            response = requests.post(
                f"{self.base_url}/summarize",
                json={"paper_id": paper_id},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Summarization failed: {str(e)}"}
    
    def assist(self, topic: str) -> Dict[str, Any]:
        """Get research assistance on a topic"""
        try:
            response = requests.post(
                f"{self.base_url}/assist",
                json={"topic": topic},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Assistance failed: {str(e)}"}
    
    def create_workspace(self, name: str) -> Dict[str, Any]:
        """Create a new workspace"""
        try:
            response = requests.post(
                f"{self.base_url}/workspace/create",
                json={"name": name},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Workspace creation failed: {str(e)}"}
    
    def list_workspaces(self) -> Dict[str, Any]:
        """List all workspaces"""
        try:
            response = requests.get(
                f"{self.base_url}/workspace/list",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Workspace listing failed: {str(e)}"}
    
    def add_paper_to_workspace(self, workspace_id: str, paper_id: str) -> Dict[str, Any]:
        """Add a paper to a workspace"""
        try:
            response = requests.post(
                f"{self.base_url}/workspace/add-paper",
                json={
                    "workspace_id": workspace_id,
                    "paper_id": paper_id
                },
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Adding paper to workspace failed: {str(e)}"}

# Global API client instance
api_client = APIClient()
