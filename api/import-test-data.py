from sqlmodel import Session
from src.db import engine, init_db
from src.projects import Project
from src.users import User
from src.items import Item
from src.events import Event
from src.feedbacks import Feedback

with Session(engine) as session:
    init_db()

    project1 = Project(
        name="project 1",
        features={
            "test": "import-test-data",
        },
    )

    user1 = User(
        project=project1,
        name="user 1",
        features={
            "test": "import-test-data",
        },
    )

    item1 = Item(
        project=project1,
        name="user 1",
        features={
            "test": "import-test-data",
        },
    )

    event1 = Event(
        project_name=project1.name,
        user=user1,
        name="event 1",
        features={
            "test": "import-test-data",
        },
    )

    feedback1 = Feedback(
        project_name=project1.name,
        user=user1,
        name="feedback 1",
        features={
            "test": "import-test-data",
        },
        value=3,
    )

    print("project 1", project1)
    print("user 1", user1)
    print("item 1", item1)
    print("event 1", event1)
    print("feedback 1", feedback1)

    session.add(project1)
    session.add(user1)
    session.add(item1)
    session.add(event1)
    session.add(feedback1)
    session.commit()

    session.refresh(project1)
    session.refresh(user1)
    session.refresh(item1)
    session.refresh(event1)
    session.refresh(feedback1)

    print("project 1", project1)
    print("user 1", user1)
    print("item 1", item1)
    print("event 1", event1)
    print("feedback 1", feedback1)
