# ResearchHub AI - Frontend Documentation

## 🚀 Overview

ResearchHub AI is a professional, multi-page Streamlit frontend for intelligent research paper management and analysis. It connects to a FastAPI backend and provides a modern SaaS-like experience for researchers.

**Live at:** http://localhost:8504

## 📋 Features

### 🏠 Home/Dashboard
- Welcome message and system status indicator
- Key statistics: Total papers uploaded, Total workspaces
- Recent activity showing recently uploaded papers
- Quick action buttons for main features
- Modern gradient cards with metrics
- Professional SaaS-style layout

### 💬 Chat with AI
- ChatGPT-style conversation interface
- Chat bubbles with role-based styling (user vs assistant)
- Persistent chat history stored locally
- Scrollable conversation area
- Clear chat button to reset conversation
- Export chat functionality
- Loading indicators while AI responds

### 📚 Research Library (Uploads)
- Upload and manage research papers
- Persistent paper library (survives server restart)
- Automatic metadata storage in `data/papers.json`
- Paper cards showing:
  - Paper ID (clearly visible and copyable)
  - Title
  - Upload date
  - Character count
- Advanced features:
  - Search papers by title or ID
  - Sort by: Most Recent, Oldest First, Alphabetical
  - Action buttons: Chat with Paper, Summarize, Add to Workspace, Copy ID
  - Library statistics (total papers, total characters, average size)

### 🔍 Discover Papers
- Search for research papers from arXiv and other sources
- Advanced filtering by:
  - Paper type (Research, Review, Survey, Preprint)
  - Publication year range
  - Sort options (Relevance, Most Recent, Most Cited)
- Professional result cards showing:
  - Title (clickable)
  - Authors list
  - Publication date
  - Summary preview
  - PDF link
- Action buttons: View PDF, Save Paper, Add to Favorites, Add to Workspace
- Featured research categories for quick exploration

### 📋 Summarize Paper
- Select from uploaded papers
- Summary length options: Short, Medium, Long
- Focus area selection: Key Findings, Methodology, Conclusions, etc.
- AI-generated intelligent summaries
- Export options: Copy to clipboard, Download as text
- Follow-up actions: Chat about paper, Add to workspace, Find related papers

### 🎓 Research Assistant
- Enter research topics for intelligent analysis
- Customizable analysis depth: Quick, Detailed, Comprehensive
- Select analysis components: Literature Review, Gaps, Ideas, Innovations
- Structured output including:
  - Research summary
  - Identified research gaps
  - Innovation ideas
  - Future directions
- Export analysis results
- Discover related papers
- Example topics for quick start

### 🗂️ Workspace Management
- Create new workspaces with:
  - Name and description
  - Tags for organization
  - Privacy settings (Private, Shared, Public)
- View all workspaces with:
  - Paper count per workspace
  - Creation date
  - Quick access buttons
- Search and filter workspaces
- View workspace details:
  - List all papers in workspace
  - Add multiple papers at once
  - View metadata
- Organize research by project/topic

## 📁 Project Structure

```
frontend/
├── app.py                          # Main entry point with routing
├── pages/                          # Page modules
│   ├── __init__.py
│   ├── home.py                    # Dashboard/Home page
│   ├── chat.py                    # Chat interface
│   ├── uploads.py                 # Paper library
│   ├── discover.py                # Paper discovery
│   ├── summarize.py               # Paper summarization
│   ├── research_assistant.py       # Research assistance
│   └── workspace.py               # Workspace management
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── api.py                     # API client for backend
│   └── storage.py                 # Local data persistence
├── data/                           # Persistent data storage
│   ├── papers.json                # Uploaded papers metadata
│   ├── workspaces.json            # Workspace definitions
│   └── chats.json                 # Chat history
├── requirements.txt               # Python dependencies
└── README.md                       # This file
```

## 🔧 Technology Stack

- **Frontend Framework**: Streamlit
- **API Client**: Python Requests
- **Data Persistence**: JSON files
- **Backend**: FastAPI (external)
- **Database**: ChromaDB (external, via backend)

## 📦 Dependencies

```
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## 🚀 Installation & Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8504` (or the next available port)

## 🔐 Architecture Highlights

### Clean Modular Design
- **app.py**: Main entry point handling navigation and routing
- **pages/**: Each feature as a separate, reusable module
- **utils/api.py**: Centralized API client for all backend calls
- **utils/storage.py**: Persistent data management layer

### Session State Management
- Persistent chat history
- Selected paper/workspace tracking
- Navigation state

### Data Persistence
- Papers metadata stored in `data/papers.json`
- Chat history stored in `data/chats.json`
- Workspaces stored in `data/workspaces.json`
- Survives Streamlit server restart

### Error Handling
- Graceful API error handling
- User-friendly error messages
- Fallback options for failed operations

### Modern UI/UX
- Consistent gradient color scheme (Purple/Blue)
- Responsive layout using Streamlit columns
- Loading spinners during API calls
- Success/warning/error notifications
- Professional card-based design
- Smooth transitions and hover effects

## 💾 Data Storage

### Papers Storage (`data/papers.json`)
```json
{
  "paper_id": "unique_id",
  "title": "Paper Title",
  "filename": "paper.pdf",
  "char_count": 50000,
  "upload_timestamp": "2026-02-25T10:30:00.000000",
  "status": "uploaded"
}
```

### Workspaces Storage (`data/workspaces.json`)
```json
{
  "workspace_id": "ws_123",
  "name": "AI Research 2024",
  "description": "...",
  "tags": ["AI", "ML"],
  "visibility": "Private",
  "papers": ["paper_id_1", "paper_id_2"],
  "created_timestamp": "2026-02-25T10:00:00.000000"
}
```

### Chat History (`data/chats.json`)
```json
{
  "main": [
    {
      "role": "user",
      "content": "What is this paper about?",
      "timestamp": "2026-02-25T10:30:00.000000"
    },
    {
      "role": "assistant",
      "content": "This paper discusses...",
      "timestamp": "2026-02-25T10:30:05.000000"
    }
  ]
}
```

## 🔗 Backend Integration

The frontend communicates with FastAPI backend at `http://127.0.0.1:8000`

### Available Endpoints
- `POST /chat` - Send a message to AI
- `POST /upload` - Upload a research paper
- `POST /discover` - Discover papers by query
- `POST /summarize` - Get summary of a paper
- `POST /assist` - Get research assistance
- `POST /workspace/create` - Create a workspace
- `GET /workspace/list` - List all workspaces
- `POST /workspace/add-paper` - Add paper to workspace

## 🎨 Styling & Customization

The app uses custom CSS for:
- Gradient buttons with hover effects
- Sidebar gradient background
- Card-based layouts
- Smooth transitions

To customize colors, edit the gradient values in `app.py` and individual page files:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🐛 Troubleshooting

### Streamlit Port Already in Use
```bash
streamlit run app.py --server.port 8505
```

### Data/Folder Not Found
The app automatically creates the `data/` folder on first run.

### API Connection Error
Ensure the FastAPI backend is running at `http://127.0.0.1:8000`

### Chat Not Loading History
Clear cache: `streamlit cache clear`

## 📚 Usage Tips

### For Researchers
1. Start by uploading your research papers
2. Use Chat to discuss papers with AI
3. Use Summarize for quick overviews
4. Organize related papers in Workspaces
5. Use Research Assistant for trend analysis

### For Developers
1. Add new pages by creating files in `pages/` with a `show()` function
2. Add new API calls to `utils/api.py`
3. Update routing in `app.py`
4. Maintain data in `utils/storage.py`

## 🔮 Future Features

Planned enhancements:
- [ ] User authentication
- [ ] Cloud deployment
- [ ] Collaboration features
- [ ] Advanced paper analytics
- [ ] Citation management
- [ ] Export to various formats
- [ ] Integration with arXiv API
- [ ] Paper recommendations based on history
- [ ] Custom AI model selection
- [ ] Batch operations

## 📝 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure code follows the modular pattern
5. Test thoroughly
6. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 👨‍💻 Development Notes

### Code Standards
- Use descriptive function names
- Add docstrings to all functions
- Keep modules under 500 lines
- Use type hints where possible
- Follow PEP 8 style guide

### Testing
- Test each page independently
- Verify data persistence
- Test API error handling
- Check responsive layout

### Performance
- Lazy load data
- Cache API responses where appropriate
- Minimize reruns
- Optimize images and media

---

**Built with ❤️ for researchers using Streamlit & FastAPI**
