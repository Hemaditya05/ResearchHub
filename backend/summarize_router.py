from fastapi import APIRouter
from pydantic import BaseModel

from agent import agent_answer


router = APIRouter()


class SummarizeRequest(BaseModel):
    paper_id: str


@router.post("/summarize")
async def summarize_paper(request: SummarizeRequest):

    question = f"Summarize the research paper with paper id {request.paper_id}"

    answer = agent_answer(question)

    return {
        "summary": answer
    }
