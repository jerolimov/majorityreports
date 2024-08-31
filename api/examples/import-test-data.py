from sqlmodel import Session
from src.db import init_db, get_engine
from src.namespaces.entity import NamespaceEntity
from src.actors.entity import ActorEntity
from src.items.entity import ItemEntity
from src.events.entity import EventEntity
from src.feedbacks.entity import FeedbackEntity


init_db()

with Session(get_engine()) as session:
    namespace1 = NamespaceEntity(
        name="namespace-1",
        labels={
            "test": "import-test-data",
        },
    )
    namespace2 = NamespaceEntity(
        name="namespace-2",
        labels={
            "test": "import-test-data",
        },
    )

    actor1 = ActorEntity(
        namespace=namespace1.name,
        name="actor-1",
        labels={
            "test": "import-test-data",
        },
    )
    actor2 = ActorEntity(
        namespace=namespace1.name,
        name="actor-2",
        labels={
            "test": "import-test-data",
        },
    )

    item1 = ItemEntity(
        namespace=namespace1.name,
        name="item-1",
        labels={
            "test": "import-test-data",
        },
    )
    item2 = ItemEntity(
        namespace=namespace1.name,
        name="item-2",
        labels={
            "test": "import-test-data",
        },
    )

    event1 = EventEntity(
        namespace=namespace1.name,
        name="same-event-name",
        actor="actor-1",
        labels={
            "test": "import-test-data",
        },
    )
    event2 = EventEntity(
        namespace=namespace1.name,
        name="same-event-name",
        # event without actor
        labels={
            "test": "import-test-data",
        },
    )

    feedback1 = FeedbackEntity(
        namespace=namespace1.name,
        name="same-feedback-name",
        actor="actor-1",
        item="item-1",
        labels={
            "test": "import-test-data",
        },
        value=3,
    )
    feedback2 = FeedbackEntity(
        namespace=namespace1.name,
        name="same-feedback-name",
        actor="actor-1",
        item="item-2",
        labels={
            "test": "import-test-data",
        },
        value=4,
    )

    print("namespace 1", namespace1)
    print("namespace 2", namespace2)
    print("actor 1", actor1)
    print("actor 2", actor2)
    print("item 1", item1)
    print("item 2", item2)
    print("event 1", event1)
    print("event 2", event2)
    print("feedback 1", feedback1)
    print("feedback 2", feedback2)

    session.add(namespace1)
    session.add(namespace2)
    session.add(actor1)
    session.add(actor2)
    session.add(item1)
    session.add(item2)
    session.add(event1)
    session.add(event2)
    session.add(feedback1)
    session.add(feedback2)
    session.commit()

    session.refresh(namespace1)
    session.refresh(namespace2)
    session.refresh(actor1)
    session.refresh(actor2)
    session.refresh(item1)
    session.refresh(item2)
    session.refresh(event1)
    session.refresh(event2)
    session.refresh(feedback1)
    session.refresh(feedback2)

    print("namespace 1", namespace1)
    print("namespace 2", namespace2)
    print("actor 1", actor1)
    print("actor 2", actor2)
    print("item 1", item1)
    print("item 2", item2)
    print("event 1", event1)
    print("event 2", event2)
    print("feedback 1", feedback1)
    print("feedback 2", feedback2)
