from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session, select, func

from ..db import get_session
from ..namespaces.entity import NamespaceEntity as Namespace
from ..actors.entity import ActorEntity as Actor
from ..items.entity import ItemEntity as Item
from ..events.entity import EventEntity as Event
from ..feedbacks.entity import FeedbackEntity as Feedback


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
    namespaceCountSelect = select(func.count("*")).select_from(Namespace)
    actorsCountSelect = select(func.count("*")).select_from(Actor)
    itemsCountSelect = select(func.count("*")).select_from(Item)
    eventsCountSelect = select(func.count("*")).select_from(Event)
    feedbacksCountSelect = select(func.count("*")).select_from(Feedback)

    if namespace_name is not None:
        actorsCountSelect = actorsCountSelect.where(
            Actor.namespace_name == namespace_name
        )
        itemsCountSelect = itemsCountSelect.where(Item.namespace_name == namespace_name)
        eventsCountSelect = eventsCountSelect.where(
            Event.namespace_name == namespace_name
        )
        feedbacksCountSelect = feedbacksCountSelect.where(
            Feedback.namespace_name == namespace_name
        )

    stats = Stats()
    if namespace_name is None:
        stats.namespaces = session.exec(namespaceCountSelect).one()
    stats.actors = session.exec(actorsCountSelect).one()
    stats.items = session.exec(itemsCountSelect).one()
    stats.events = session.exec(eventsCountSelect).one()
    stats.feedbacks = session.exec(feedbacksCountSelect).one()

    return stats
