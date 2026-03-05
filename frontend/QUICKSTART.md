# ResearchHub AI - Quick Start Guide

## 🎯 Getting Started in 2 Minutes

### Prerequisites
- Python 3.8+
- ResearchHub AI backend running at `http://127.0.0.1:8000`

### Step 1: Start the Frontend

```bash
cd frontend
streamlit run app.py
```

Your app will open at: **http://localhost:8504**

### Step 2: Explore the Features

#### 📚 Upload Your First Paper
1. Click **Uploads** in the sidebar
2. Choose a PDF file
3. Click **Upload Paper**
4. Your paper is now saved (permanently!)

#### 💬 Chat with AI
1. Click **Chat** in the sidebar
2. Ask a question about your research
3. Get instant AI responses
4. Your conversation is automatically saved

#### 📋 Summarize a Paper
1. Go to **Summarize**
2. Select a paper from your library
3. Choose summary length and focus areas
4. Get an instant summary!

#### 🔍 Discover Papers
1. Click **Discover**
2. Search for research topics
3. Filter by year, type, etc.
4. Save papers directly to your library

#### 🗂️ Organize with Workspaces
1. Go to **Workspace**
2. Create a new workspace
3. Add papers to organize by project
4. Keep your research organized

#### 🎓 Get Research Insights
1. Click **Research Assistant**
2. Enter a research topic
3. Get structured analysis with:
   - Research summary
   - Gaps in current research
   - Innovation ideas
   - Future directions

## 💡 Key Features

### ✨ Data Persistence
All your data is **automatically saved** and survives server restart:
- Papers stay in your library
- Chat history is preserved
- Workspaces are remembered

### 🎨 Modern UI
- Gradient purple/blue design
- Responsive layout
- Smooth animations
- Professional cards

### 🔗 Seamless Integration
- Connects to FastAPI backend
- Supports all major endpoints
- Error handling built-in

### ⚡ Fast & Responsive
- Instant paper uploads
- Real-time AI responses
- Smooth navigation

## 📱 Interface Overview

### Sidebar Navigation
```
🚀 ResearchHub AI
├── 🏠 Home
├── 💬 Chat
├── 📚 Uploads
├── 🔍 Discover
├── 📋 Summarize
├── 🎓 Research Assistant
└── 🗂️ Workspace
```

### Home Dashboard Shows
- ✅ Backend Status
- 📄 Total Papers Uploaded
- 🗂️ Total Workspaces
- ⭐ AI Status
- 📋 Recent Activity

## 🔧 Configuration

### Change Backend URL
Edit `utils/api.py`:
```python
BASE_URL = "http://127.0.0.1:8000"  # Change this
```

### Change Streamlit Port
```bash
streamlit run app.py --server.port 8505
```

### Increase Timeout for Large Files
Edit `utils/api.py`:
```python
self.timeout = 60  # Increase from 30
```

## 🚨 Common Issues

### Problem: "Connection refused"
**Solution:** Make sure FastAPI backend is running
```bash
cd backend
uvicorn main:app --reload
```

### Problem: Port already in use
**Solution:** Use a different port
```bash
streamlit run app.py --server.port 8505
```

### Problem: Data not persisting
**Solution:** Check `data/` folder exists and is writable

### Problem: Chat not showing history
**Solution:** Clear Streamlit cache
```bash
streamlit cache clear
```

## 📊 Data Files

Your data is stored in:
```
frontend/data/
├── papers.json          # Your uploaded papers
├── workspaces.json      # Your workspaces
└── chats.json           # Chat history
```

You can backup these files to preserve your research!

## 🎮 Keyboard Shortcuts

While using the app:
- `Ctrl + Q` - Toggle sidebar
- Click "Clear Chat" - Clear conversation
- Click "Copy ID" - Copy paper ID to clipboard

## 💬 Chat Examples

Try asking:
- "What are the key findings from this paper?"
- "Summarize the methodology section"
- "Compare papers in my library"
- "What's trending in AI research?"
- "Help me find research gaps"

## 🚀 Pro Tips

1. **Organize with Workspaces**: Group related papers by project
2. **Use Chat for Deep Dives**: Discuss papers in detail with AI
3. **Export Regularly**: Download your summaries and analysis
4. **Backup Your Data**: Copy the `data/` folder periodically
5. **Explore Discover**: Find new papers while researching

## 📱 Mobile Access

You can access from other devices on your network:
- **Phone/Tablet**: http://192.168.2.224:8504
- **Another Computer**: http://<your-ip>:8504

## 🔐 Data Privacy

- All data stored locally (not sent to cloud)
- Papers stored securely in `data/` folder
- Chat history private and local
- Only connects to your backend server

## 🆘 Need Help?

1. Check the full **README.md** in frontend folder
2. Review **Backend** logs for API issues
3. Check browser console for frontend errors
4. Ensure backend is responding: `curl http://127.0.0.1:8000/health`

## 🎓 Learning Path

1. **Day 1**: Upload papers → Explore library → Chat about them
2. **Day 2**: Try Summarize → Use Discover → Organize with Workspaces
3. **Day 3**: Use Research Assistant → Get insights → Export reports
4. **Day 4+**: Advanced workflows → Collaboration → Custom analysis

---

**Happy researching! 🚀**

For more details, see the full **README.md** file.
