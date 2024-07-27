from sqlmodel import Session
from src.db import engine, init_db
from src.namespaces import Namespace
from src.actor import Actor
from src.items import Item
from src.events import Event
from src.feedbacks import Feedback

with Session(engine) as session:
    init_db()

    namespace1 = Namespace(
        name="namespace 1",
        labels={
            "test": "import-test-data",
        },
    )
    namespace2 = Namespace(
        name="namespace 2",
        labels={
            "test": "import-test-data",
        },
    )

    actor1 = Actor(
        namespace=namespace1,
        name="actor 1",
        labels={
            "test": "import-test-data",
        },
    )
    actor2 = Actor(
        namespace=namespace1,
        name="actor 2",
        labels={
            "test": "import-test-data",
        },
    )

    item1 = Item(
        namespace=namespace1,
        name="item 1",
        labels={
            "test": "import-test-data",
        },
    )
    item2 = Item(
        namespace=namespace1,
        name="item 2",
        labels={
            "test": "import-test-data",
        },
    )

    event1 = Event(
        namespace=namespace1,
        name="same-event-name",
        actor=actor1,
        labels={
            "test": "import-test-data",
        },
    )
    event2 = Event(
        namespace=namespace1,
        name="same-event-name",
        # event without actor
        labels={
            "test": "import-test-data",
        },
    )

    feedback1 = Feedback(
        namespace=namespace1,
        name="same-feedback-name",
        actor=actor1,
        labels={
            "test": "import-test-data",
        },
        value=3,
    )
    feedback2 = Feedback(
        namespace=namespace1,
        name="same-feedback-name",
        actor=actor1,
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
