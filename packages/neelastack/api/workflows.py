import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Workflow, WorkflowRun
from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.workflows.executor import (
    WorkflowExecutor,
    WorkflowExecutionError,
)

router = APIRouter(prefix="/workflows", tags=["workflows"])


def _workflow_response(workflow):
    return {
        "id": workflow.id,
        "name": workflow.name,
        "definition_json": workflow.definition_json,
        "created_at": workflow.created_at,
    }


def _run_response(run):
    return {
        "id": run.id,
        "workflow_id": run.workflow_id,
        "status": run.status,
        "input_json": run.input_json,
        "output_json": run.output_json,
        "error": run.error,
        "created_at": run.created_at,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
    }


@router.get("")
def list_workflows(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    workflows = db.scalars(
        select(Workflow)
        .where(Workflow.user_id == user.id)
        .order_by(Workflow.id.desc())
    ).all()

    return {
        "workflows": [
            _workflow_response(workflow)
            for workflow in workflows
        ]
    }


@router.post("")
def create_workflow(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = data.get("name")
    definition_json = data.get("definition_json", "{}")

    if not name or not name.strip():
        raise HTTPException(
            status_code=422,
            detail="Workflow name is required",
        )

    if not isinstance(definition_json, str):
        raise HTTPException(
            status_code=422,
            detail="definition_json must be a JSON string",
        )

    try:
        json.loads(definition_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="definition_json must contain valid JSON",
        )

    workflow = Workflow(
        user_id=user.id,
        name=name.strip(),
        definition_json=definition_json,
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return _workflow_response(workflow)


@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    workflow = db.scalar(
        select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id,
        )
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    return _workflow_response(workflow)


@router.post("/{workflow_id}/run")
async def run_workflow(
    workflow_id: int,
    data: dict | None = None,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    workflow = db.scalar(
        select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id,
        )
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    payload = data or {}

    try:
        definition = json.loads(workflow.definition_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Workflow definition contains invalid JSON",
        )

    if not isinstance(definition, dict):
        raise HTTPException(
            status_code=422,
            detail="Workflow definition must be a JSON object",
        )

    steps = definition.get("steps", [])

    if not isinstance(steps, list):
        raise HTTPException(
            status_code=422,
            detail="Workflow definition 'steps' must be a list",
        )

    now = datetime.now(timezone.utc)

    run = WorkflowRun(
        workflow_id=workflow.id,
        user_id=user.id,
        status="pending",
        input_json=json.dumps(payload),
        output_json="{}",
        created_at=now,
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        db.commit()

        executor = WorkflowExecutor()

        output = await executor.run(
            steps,
            context=payload,
        )

        run.status = "completed"
        run.output_json = json.dumps(output)
        run.completed_at = datetime.now(timezone.utc)
        run.error = None

        db.commit()
        db.refresh(run)

        return _run_response(run)

    except WorkflowExecutionError as exc:
        run.status = "failed"
        run.error = str(exc)
        run.completed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(run)

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception as exc:
        db.rollback()

        run = db.scalar(
            select(WorkflowRun).where(
                WorkflowRun.id == run.id,
                WorkflowRun.user_id == user.id,
            )
        )

        if run:
            run.status = "failed"
            run.error = str(exc)
            run.completed_at = datetime.now(timezone.utc)
            db.commit()

        raise HTTPException(
            status_code=500,
            detail="Workflow execution failed",
        )


@router.get("/{workflow_id}/runs")
def list_workflow_runs(
    workflow_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    workflow = db.scalar(
        select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id,
        )
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    runs = db.scalars(
        select(WorkflowRun)
        .where(
            WorkflowRun.workflow_id == workflow_id,
            WorkflowRun.user_id == user.id,
        )
        .order_by(WorkflowRun.id.desc())
    ).all()

    return {
        "runs": [
            _run_response(run)
            for run in runs
        ]
    }


@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    workflow = db.scalar(
        select(Workflow).where(
            Workflow.id == workflow_id,
            Workflow.user_id == user.id,
        )
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    db.delete(workflow)
    db.commit()

    return {
        "deleted": True,
        "workflow_id": workflow_id,
    }
