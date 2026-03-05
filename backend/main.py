from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chat import router as chat_router
from discovery_router import router as discovery_router
from workspace_router import router as workspace_router
from summarize_router import router as summarize_router
from assistant_router import router as assistant_router
 
from upload import router as upload_router


app = FastAPI(
    title="ResearchHub AI",
    version="3.0",
    description="Super-Cool Agentic AI Research Assistant"
)


# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include upload router
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(discovery_router)
app.include_router(workspace_router)
app.include_router(summarize_router)
app.include_router(assistant_router)



# Root endpoint
@app.get("/")
def home():
    return {
        "status": "ResearchHub AI backend running",
        "features": [
            "PDF Upload",
            "Semantic Search",
            "AI Embeddings",
            "Agentic AI Ready"
        ]
    }
