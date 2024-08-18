from fastapi import APIRouter, Depends
from sqlmodel import (
    SQLModel,
    Session,
    select,
    null,
)
from sqlalchemy import func
from typing import Iterable

from ..db import get_session
from .entity import ActorEntity as Actor


class ActorsResult(SQLModel):
    count: int | None = None  # fix types
    items: Iterable[Actor] | None = None


router = APIRouter()


@router.get("")
def read_actors(
    namespace_name: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> ActorsResult:
    countSelect = select(func.count("*")).select_from(Actor)
    itemsSelect = select(Actor).offset(offset).limit(limit)

    if namespace_name is not None:
        countSelect = countSelect.where(Actor.namespace_name == namespace_name)
        itemsSelect = itemsSelect.where(Actor.namespace_name == namespace_name)

    countSelect = countSelect.where(Actor.deletedTimestamp == null())
    itemsSelect = itemsSelect.where(Actor.deletedTimestamp == null())

    result = ActorsResult()
    result.count = session.exec(countSelect).one()
    result.items = session.exec(itemsSelect).all()
    return result
