from sqlmodel import Session, select, func

from .db import engine
from .projects import Project
from .users import User
from .items import Item
from .events import Event
from .feedbacks import Feedback


def init_testdata() -> None:
    with Session(engine) as session:
        projectCount = session.scalar(select(func.count()).select_from(Item))
        if projectCount == 0:
            session.add(Project(ref="my-project", name="My project"))

        userCount = session.scalar(select(func.count()).select_from(User))
        if userCount == 0:
            session.add(User(ref="user-a", name="user a"))
            session.add(User(ref="user-b", name="user b"))
            session.add(User(ref="user-c", name="user c"))

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
