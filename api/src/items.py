import uuid
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select, JSON, Relationship
from typing import Iterable, Dict
from .db import get_session
from .projects import Project


class Item(SQLModel, table=True):
    uid: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    project_name: str = Field(foreign_key="project.name")
    project: Project = Relationship()
    name: str = Field()
    features: Dict[str, str] = Field(default={}, sa_type=JSON)


router = APIRouter()


@router.post("")
def create_item(newItem: Item, session: Session = Depends(get_session)) -> Item:
    item = Item()
    item.name = newItem.name
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("")
def get_items(session: Session = Depends(get_session)) -> Iterable[Item]:
    statement = select(Item)
    return session.exec(statement).all()


@router.get("/{item_id}")
def get_item_by_item_id(item_id: int, session: Session = Depends(get_session)) -> Item:
    item = session.get_one(Item, item_id)
    return item


@router.put("/{item_id}")
def update_item_by_item_id(
    item_id: int, updateItem: Item, session: Session = Depends(get_session)
) -> Item:
    item = session.get_one(Item, item_id)
    if name := updateItem.name:
        item.name = name
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_item_by_item_id(
    item_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    item = session.get_one(Item, item_id)
    session.delete(item)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Item deleted"}
    )
