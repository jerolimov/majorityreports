from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


router = APIRouter()


@router.post("")
def create_user(newUser: User, session: Session = Depends(get_session)) -> User:
    user = User()
    user.name = newUser.name
    if isinstance(newUser.done, bool):
        user.done = newUser.done
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
    if done := updateUser.done:
        user.done = done
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
