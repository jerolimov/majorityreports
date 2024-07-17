from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


router = APIRouter()


@router.post("")
def create_project(
    newProject: Project, session: Session = Depends(get_session)
) -> Project:
    project = Project()
    project.name = newProject.name
    if isinstance(newProject.done, bool):
        project.done = newProject.done
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
    if done := updateProject.done:
        project.done = done
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
