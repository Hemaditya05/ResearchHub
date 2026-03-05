import json
import os
import uuid

WORKSPACE_FILE = "workspaces.json"


def load_workspaces():

    if not os.path.exists(WORKSPACE_FILE):
        return {}

    with open(WORKSPACE_FILE, "r") as f:
        return json.load(f)


def save_workspaces(data):

    with open(WORKSPACE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def create_workspace(name):

    data = load_workspaces()

    workspace_id = str(uuid.uuid4())

    data[workspace_id] = {
        "name": name,
        "papers": []
    }

    save_workspaces(data)

    return workspace_id


def add_paper_to_workspace(workspace_id, paper_id):

    data = load_workspaces()

    if workspace_id not in data:
        return False

    data[workspace_id]["papers"].append(paper_id)

    save_workspaces(data)

    return True


def get_workspaces():

    return load_workspaces()
