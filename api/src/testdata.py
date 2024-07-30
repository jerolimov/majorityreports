from sqlmodel import Session, select, func

from .db import engine
from .namespaces import Namespace, read_namespace
from .actors import Actor, read_actor
from .items import Item, read_item
from .events import Event
from .feedbacks import Feedback


def init_testdata() -> None:
    with Session(engine) as session:
        namespaceCount = session.scalar(select(func.count()).select_from(Item))
        if namespaceCount == 0:
            session.add(Namespace(name="default"))

        namespace = read_namespace("default", session)

        actorCount = session.scalar(select(func.count()).select_from(Actor))
        if actorCount == 0:
            session.add(Actor(namespace=namespace, name="actor-a"))
            session.add(Actor(namespace=namespace, name="actor-b"))
            session.add(Actor(namespace=namespace, name="actor-c"))

        itemCount = session.scalar(select(func.count()).select_from(Item))
        if itemCount == 0:
            session.add(Item(namespace=namespace, name="item-a"))
            session.add(Item(namespace=namespace, name="item-b"))
            session.add(Item(namespace=namespace, name="item-c"))

        actorA = read_actor("default", "actor-a", session)
        actorB = read_actor("default", "actor-b", session)
        itemA = read_item("default", "item-a", session)
        itemB = read_item("default", "item-b", session)

        eventCount = session.scalar(select(func.count()).select_from(Event))
        if eventCount == 0:
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-a-for-item-a",
                    actor=actorA,
                    item=itemA,
                    type="watched",
                )
            )
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-a-for-item-b",
                    actor=actorA,
                    item=itemB,
                    type="watched",
                )
            )
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-b-for-item-a",
                    actor=actorB,
                    item=itemA,
                    type="watched",
                )
            )
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-b-for-item-b",
                    actor=actorB,
                    item=itemB,
                    type="canceled",
                )
            )

        feedbackCount = session.scalar(select(func.count()).select_from(Feedback))
        if feedbackCount == 0:
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-a-for-item-a",
                    actor=actorA,
                    item=itemA,
                    value=3,
                )
            )
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-a-for-item-b",
                    actor=actorA,
                    item=itemB,
                    value=4,
                )
            )
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-b-for-item-a",
                    actor=actorB,
                    item=itemA,
                    value=5,
                )
            )
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-b-for-item-b",
                    actor=actorB,
                    item=itemB,
                    value=5,
                )
            )

        session.commit()
