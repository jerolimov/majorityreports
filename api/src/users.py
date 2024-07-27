import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict
from .db import get_session
from .projects import Project


class User(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    project_name: str = Field(foreign_key="project.name")
    project: Project = Relationship()
    name: str = Field()
    features: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_user(newUser: User, session: Session = Depends(get_session)) -> User:
    user = User()
    user.name = newUser.name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("")
def get_users(session: Session = Depends(get_session)) -> Iterable[User]:
    statement = select(User)
    return session.exec(statement).all()


@router.get("/{user_id}")
def get_user_by_user_id(user_id: int, session: Session = Depends(get_session)) -> User:
    user = session.get_one(User, user_id)
    return user


@router.put("/{user_id}")
def update_user_by_user_id(
    user_id: int, updateUser: User, session: Session = Depends(get_session)
) -> User:
    user = session.get_one(User, user_id)
    if name := updateUser.name:
        user.name = name
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user_by_user_id(
    user_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    user = session.get_one(User, user_id)
    session.delete(user)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "User deleted"}
    )
