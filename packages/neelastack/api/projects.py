from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Project
from packages.neelastack.auth.dependencies import current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
def list_projects(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    projects = db.scalars(
        select(Project)
        .where(Project.user_id == user.id)
        .order_by(Project.id.desc())
    ).all()

    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "created_at": project.created_at,
            }
            for project in projects
        ]
    }


@router.post("")
def create_project(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = data.get("name")

    if not name or not name.strip():
        raise HTTPException(
            status_code=422,
            detail="Project name is required",
        )

    project = Project(
        user_id=user.id,
        name=name.strip(),
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "name": project.name,
        "created_at": project.created_at,
    }


@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == user.id,
        )
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {
        "id": project.id,
        "name": project.name,
        "created_at": project.created_at,
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == user.id,
        )
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    db.delete(project)
    db.commit()

    return {
        "deleted": True,
        "project_id": project_id,
    }
