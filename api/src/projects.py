import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON
from typing import Iterable, Dict
from .db import get_session


class Project(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(unique=True)
    features: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_project(
    newProject: Project, session: Session = Depends(get_session)
) -> Project:
    project = Project()
    project.name = newProject.name
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("")
def get_projects(session: Session = Depends(get_session)) -> Iterable[Project]:
    statement = select(Project)
    return session.exec(statement).all()


@router.get("/{project_id}")
def get_project_by_project_id(
    project_id: int, session: Session = Depends(get_session)
) -> Project:
    project = session.get_one(Project, project_id)
    return project


@router.put("/{project_id}")
def update_project_by_project_id(
    project_id: int, updateProject: Project, session: Session = Depends(get_session)
) -> Project:
    project = session.get_one(Project, project_id)
    if name := updateProject.name:
        project.name = name
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project_by_project_id(
    project_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    project = session.get_one(Project, project_id)
    session.delete(project)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Project deleted"}
    )
