from sqlmodel import Session, select, func

from .db import engine
from .namespaces import Namespace
from .actor import Actor
from .items import Item
from .events import Event
from .feedbacks import Feedback


def init_testdata() -> None:
    with Session(engine) as session:
        namespaceCount = session.scalar(select(func.count()).select_from(Item))
        if namespaceCount == 0:
            session.add(Namespace(ref="my-namespace", name="My namespace"))

        userCount = session.scalar(select(func.count()).select_from(Actor))
        if userCount == 0:
            session.add(Actor(ref="actor-a", name="actor a"))
            session.add(Actor(ref="actor-b", name="actor b"))
            session.add(Actor(ref="actor-c", name="actor c"))

        itemCount = session.scalar(select(func.count()).select_from(Item))
        if itemCount == 0:
            session.add(Item(ref="item-a", name="item a"))
            session.add(Item(ref="item-b", name="item b"))
            session.add(Item(ref="item-c", name="item c"))

        eventCount = session.scalar(select(func.count()).select_from(Event))
        if eventCount == 0:
            session.add(Event(name="event 1"))
            session.add(Event(name="event 2"))
            session.add(Event(name="event 3"))

        feedbackCount = session.scalar(select(func.count()).select_from(Feedback))
        if feedbackCount == 0:
            session.add(Feedback(name="feedback 1"))
            session.add(Feedback(name="feedback 2"))
            session.add(Feedback(name="feedback 3"))

        session.commit()
