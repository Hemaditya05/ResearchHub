from fastapi import APIRouter
from pydantic import BaseModel

from agent import agent_answer


router = APIRouter()


class AssistRequest(BaseModel):
    topic: str


@router.post("/assist")
async def research_assistant(request: AssistRequest):

    question = f"""
Analyze the research topic: {request.topic}

Give:

1. Research summary
2. Research gaps
3. Missing features in current systems
4. Improvement ideas
5. Innovative project ideas

Answer clearly.
"""

    answer = agent_answer(question)

    return {
        "assistance": answer
    }
