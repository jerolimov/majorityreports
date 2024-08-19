from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, func

from ..db import get_session
from ..namespaces.entity import NamespaceEntity
from ..actors.entity import ActorEntity
from ..items.entity import ItemEntity
from ..events.entity import EventEntity
from ..feedbacks.entity import FeedbackEntity


class Stats(SQLModel):
    namespaces: int | None = None
    actors: int | None = None
    items: int | None = None
    events: int | None = None
    feedbacks: int | None = None


router = APIRouter()


@router.get("", response_model_exclude_none=True)
def get_stats(
    namespace_name: str | None = None,
    session: Session = Depends(get_session),
) -> Stats:
    namespaceCountSelect = select(func.count("*")).select_from(NamespaceEntity)
    actorsCountSelect = select(func.count("*")).select_from(ActorEntity)
    itemsCountSelect = select(func.count("*")).select_from(ItemEntity)
    eventsCountSelect = select(func.count("*")).select_from(EventEntity)
    feedbacksCountSelect = select(func.count("*")).select_from(FeedbackEntity)

    if namespace_name is not None:
        actorsCountSelect = actorsCountSelect.where(
            ActorEntity.namespace == namespace_name
        )
        itemsCountSelect = itemsCountSelect.where(
            ItemEntity.namespace == namespace_name
        )
        eventsCountSelect = eventsCountSelect.where(
            EventEntity.namespace == namespace_name
        )
        feedbacksCountSelect = feedbacksCountSelect.where(
            FeedbackEntity.namespace == namespace_name
        )

    stats = Stats()
    if namespace_name is None:
        stats.namespaces = session.exec(namespaceCountSelect).one()
    stats.actors = session.exec(actorsCountSelect).one()
    stats.items = session.exec(itemsCountSelect).one()
    stats.events = session.exec(eventsCountSelect).one()
    stats.feedbacks = session.exec(feedbacksCountSelect).one()

    return stats
