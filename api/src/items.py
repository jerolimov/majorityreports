from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


router = APIRouter()


@router.post("")
def create_item(newItem: Item, session: Session = Depends(get_session)) -> Item:
    item = Item()
    item.name = newItem.name
    if isinstance(newItem.done, bool):
        item.done = newItem.done
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
    if done := updateItem.done:
        item.done = done
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
