import json
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from apps.api.main import app
from packages.neelastack.auth.jwt import create_token
from packages.neelastack.auth import hash_password
from packages.neelastack.database.models import User, WorkflowRun
from packages.neelastack.database.session import SessionLocal


def _create_test_user():
    db = SessionLocal()

    user = User(
        email=f"workflow-test-{uuid4().hex}@example.com",
        password_hash=hash_password("test-password"),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id)
    user_id = user.id
    db.close()

    return user_id, token


def test_workflow_run_success():
    user_id, token = _create_test_user()

    client = TestClient(app)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    workflow_response = client.post(
        "/workflows",
        headers=headers,
        json={
            "name": "Integration Workflow",
            "definition_json": '{"steps":["collect","analyze","review"]}',
        },
    )

    assert workflow_response.status_code == 200

    workflow = workflow_response.json()
    workflow_id = workflow["id"]

    run_response = client.post(
        f"/workflows/{workflow_id}/run",
        headers=headers,
        json={"input": "integration test"},
    )

    assert run_response.status_code == 200

    run = run_response.json()

    assert run["workflow_id"] == workflow_id
    assert run["status"] == "completed"
    assert run["error"] is None

    assert '"collect"' in run["output_json"]
    assert '"analyze"' in run["output_json"]
    assert '"review"' in run["output_json"]

    db = SessionLocal()

    stored_run = db.scalar(
        select(WorkflowRun).where(
            WorkflowRun.id == run["id"],
            WorkflowRun.user_id == user_id,
        )
    )

    assert stored_run is not None
    assert stored_run.status == "completed"
    assert stored_run.started_at is not None
    assert stored_run.completed_at is not None

    db.close()


def test_workflow_run_rejects_unsafe_step():
    user_id, token = _create_test_user()

    client = TestClient(app)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    workflow_response = client.post(
        "/workflows",
        headers=headers,
        json={
            "name": "Unsafe Workflow",
            "definition_json": (
                '{"steps":['
                '{"name":"safe"},'
                '{"callable":"os.system"}'
                ']}'
            ),
        },
    )

    assert workflow_response.status_code == 200

    workflow_id = workflow_response.json()["id"]

    run_response = client.post(
        f"/workflows/{workflow_id}/run",
        headers=headers,
        json={"input": "security test"},
    )

    assert run_response.status_code == 422
    assert "non-empty name" in run_response.json()["detail"]

    db = SessionLocal()

    stored_run = db.scalar(
        select(WorkflowRun).where(
            WorkflowRun.workflow_id == workflow_id,
            WorkflowRun.user_id == user_id,
        )
    )

    assert stored_run is not None
    assert stored_run.status == "failed"
    assert "non-empty name" in stored_run.error
    assert stored_run.completed_at is not None

    db.close()


def test_workflow_run_history():
    user_id, token = _create_test_user()

    client = TestClient(app)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    workflow_response = client.post(
        "/workflows",
        headers=headers,
        json={
            "name": "History Workflow",
            "definition_json": '{"steps":["one"]}',
        },
    )

    assert workflow_response.status_code == 200

    workflow_id = workflow_response.json()["id"]

    run_response = client.post(
        f"/workflows/{workflow_id}/run",
        headers=headers,
        json={"input": "history test"},
    )

    assert run_response.status_code == 200

    history_response = client.get(
        f"/workflows/{workflow_id}/runs",
        headers=headers,
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert "runs" in history
    assert len(history["runs"]) >= 1
    assert history["runs"][0]["workflow_id"] == workflow_id
    assert history["runs"][0]["status"] == "completed"
