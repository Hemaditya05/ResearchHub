from fastapi import APIRouter
from pydantic import BaseModel

from workspace import (
    create_workspace,
    add_paper_to_workspace,
    get_workspaces
)


router = APIRouter()


class WorkspaceCreateRequest(BaseModel):
    name: str


class AddPaperRequest(BaseModel):
    workspace_id: str
    paper_id: str


@router.post("/workspace/create")
async def create_new_workspace(request: WorkspaceCreateRequest):

    workspace_id = create_workspace(request.name)

    return {
        "workspace_id": workspace_id,
        "name": request.name
    }


@router.post("/workspace/add-paper")
async def add_paper(request: AddPaperRequest):

    success = add_paper_to_workspace(
        request.workspace_id,
        request.paper_id
    )

    if not success:
        return {"status": "error", "message": "Workspace not found"}

    return {"status": "success"}


@router.get("/workspace/list")
async def list_workspaces():

    return {
        "workspaces": get_workspaces()
    }
