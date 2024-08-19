from sqlmodel import Session, select, func, and_

from .db import engine
from .namespaces.entity import NamespaceEntity as Namespace
from .actors.entity import ActorEntity as Actor
from .items.entity import ItemEntity as Item
from .events.entity import EventEntity as Event
from .feedbacks.entity import FeedbackEntity as Feedback


namespace_name = "default"


def init_testdata() -> None:
    with Session(engine) as session:
        namespace = session.exec(
            select(Namespace).where(Namespace.name == namespace_name)
        ).one_or_none()
        if namespace is None:
            namespace = Namespace(
                name=namespace_name,
                labels={
                    "test": "testdata",
                },
                tags=[
                    "testdata",
                ],
                lifecycle="experiment",
            )
            session.add(namespace)
            session.commit()
            session.refresh(namespace)

        if (
            session.scalar(
                select(func.count())
                .select_from(Actor)
                .where(and_(Actor.namespace == namespace_name, Actor.name == "actor-a"))
            )
            == 0
        ):
            session.add(Actor(namespace=namespace_name, name="actor-a"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Actor)
                .where(and_(Actor.namespace == namespace_name, Actor.name == "actor-b"))
            )
            == 0
        ):
            session.add(Actor(namespace=namespace_name, name="actor-b"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Actor)
                .where(and_(Actor.namespace == namespace_name, Actor.name == "actor-c"))
            )
            == 0
        ):
            session.add(Actor(namespace=namespace_name, name="actor-c"))

        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(and_(Item.namespace == namespace_name, Item.name == "item-a"))
            )
            == 0
        ):
            session.add(Item(namespace=namespace_name, name="item-a"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(and_(Item.namespace == namespace_name, Item.name == "item-b"))
            )
            == 0
        ):
            session.add(Item(namespace=namespace_name, name="item-b"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(and_(Item.namespace == namespace_name, Item.name == "item-c"))
            )
            == 0
        ):
            session.add(Item(namespace=namespace_name, name="item-c"))

        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace == namespace_name,
                        Event.name == "event-from-actor-a-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace_name,
                    name="event-from-actor-a-for-item-a",
                    actor="actor-a",
                    item="item-a",
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace == namespace_name,
                        Event.name == "event-from-actor-a-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace_name,
                    name="event-from-actor-a-for-item-b",
                    actor="actor-a",
                    item="item-b",
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace == namespace_name,
                        Event.name == "event-from-actor-b-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace_name,
                    name="event-from-actor-b-for-item-a",
                    actor="actor-b",
                    item="item-a",
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace == namespace_name,
                        Event.name == "event-from-actor-b-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace_name,
                    name="event-from-actor-b-for-item-b",
                    actor="actor-b",
                    item="item-b",
                    type="canceled",
                )
            )

        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace == namespace_name,
                        Feedback.name == "feedback-from-actor-a-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace_name,
                    name="feedback-from-actor-a-for-item-a",
                    actor="actor-a",
                    item="item-a",
                    value=3,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace == namespace_name,
                        Feedback.name == "feedback-from-actor-a-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace_name,
                    name="feedback-from-actor-a-for-item-b",
                    actor="actor-a",
                    item="item-b",
                    value=4,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace == namespace_name,
                        Feedback.name == "feedback-from-actor-b-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace_name,
                    name="feedback-from-actor-b-for-item-a",
                    actor="actor-b",
                    item="item-a",
                    value=5,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace == namespace_name,
                        Feedback.name == "feedback-from-actor-b-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace_name,
                    name="feedback-from-actor-b-for-item-b",
                    actor="actor-b",
                    item="item-b",
                    value=5,
                )
            )

        session.commit()
