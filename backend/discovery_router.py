from fastapi import APIRouter
from pydantic import BaseModel

from discovery import search_arxiv


router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/discover")
async def discover_papers(request: SearchRequest):

    papers = search_arxiv(request.query)

    return {
        "papers": papers
    }
    