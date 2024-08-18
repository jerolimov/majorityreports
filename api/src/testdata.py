from sqlmodel import Session, select, func, and_

from .db import engine
from .namespaces.entity import NamespaceEntity as Namespace
from .actors.entity import ActorEntity as Actor
from .items.entity import ItemEntity as Item
from .events.entity import EventEntity as Event
from .feedbacks.entity import FeedbackEntity as Feedback

from .actors.crud import read_actor
from .items.crud import read_item


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
                .where(
                    and_(
                        Actor.namespace_name == namespace_name, Actor.name == "actor-a"
                    )
                )
            )
            == 0
        ):
            session.add(Actor(namespace=namespace, name="actor-a"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Actor)
                .where(
                    and_(
                        Actor.namespace_name == namespace_name, Actor.name == "actor-b"
                    )
                )
            )
            == 0
        ):
            session.add(Actor(namespace=namespace, name="actor-b"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Actor)
                .where(
                    and_(
                        Actor.namespace_name == namespace_name, Actor.name == "actor-c"
                    )
                )
            )
            == 0
        ):
            session.add(Actor(namespace=namespace, name="actor-c"))

        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(
                    and_(Item.namespace_name == namespace_name, Item.name == "item-a")
                )
            )
            == 0
        ):
            session.add(Item(namespace=namespace, name="item-a"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(
                    and_(Item.namespace_name == namespace_name, Item.name == "item-b")
                )
            )
            == 0
        ):
            session.add(Item(namespace=namespace, name="item-b"))
        if (
            session.scalar(
                select(func.count())
                .select_from(Item)
                .where(
                    and_(Item.namespace_name == namespace_name, Item.name == "item-c")
                )
            )
            == 0
        ):
            session.add(Item(namespace=namespace, name="item-c"))

        actorA = read_actor(namespace_name, "actor-a", session)
        actorB = read_actor(namespace_name, "actor-b", session)
        itemA = read_item(namespace_name, "item-a", session)
        itemB = read_item(namespace_name, "item-b", session)

        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace_name == namespace_name,
                        Event.name == "event-from-actor-a-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-a-for-item-a",
                    actor=actorA,
                    item=itemA,
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace_name == namespace_name,
                        Event.name == "event-from-actor-a-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-a-for-item-b",
                    actor=actorA,
                    item=itemB,
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace_name == namespace_name,
                        Event.name == "event-from-actor-b-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-b-for-item-a",
                    actor=actorB,
                    item=itemA,
                    type="watched",
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Event)
                .where(
                    and_(
                        Event.namespace_name == namespace_name,
                        Event.name == "event-from-actor-b-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Event(
                    namespace=namespace,
                    name="event-from-actor-b-for-item-b",
                    actor=actorB,
                    item=itemB,
                    type="canceled",
                )
            )

        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace_name == namespace_name,
                        Feedback.name == "feedback-from-actor-a-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-a-for-item-a",
                    actor=actorA,
                    item=itemA,
                    value=3,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace_name == namespace_name,
                        Feedback.name == "feedback-from-actor-a-for-item-b",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-a-for-item-b",
                    actor=actorA,
                    item=itemB,
                    value=4,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace_name == namespace_name,
                        Feedback.name == "feedback-from-actor-b-for-item-a",
                    )
                )
            )
            == 0
        ):
            session.add(
                Feedback(
                    namespace=namespace,
                    name="feedback-from-actor-b-for-item-a",
                    actor=actorB,
                    item=itemA,
                    value=5,
                )
            )
        if (
            session.scalar(
                select(func.count())
                .select_from(Feedback)
                .where(
                    and_(
                        Feedback.namespace_name == namespace_name,
                        Feedback.name == "feedback-from-actor-b-for-item-b",
                    )
                )
            )
            == 0
        ):
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
