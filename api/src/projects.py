from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ref: str
    name: str


router = APIRouter()


@router.post("")
def create_project(
    newProject: Project, session: Session = Depends(get_session)
) -> Project:
    project = Project()
    project.ref = newProject.ref
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
    if ref := updateProject.ref:
        project.ref = ref
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
