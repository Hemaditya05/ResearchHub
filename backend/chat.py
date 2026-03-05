from fastapi import APIRouter
from pydantic import BaseModel

from agent import agent_answer


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat_with_agent(request: ChatRequest):

    answer = agent_answer(request.message)

    return {
        "answer": answer
    }
