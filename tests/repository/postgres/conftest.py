import sqlalchemy
import pytest

from src.repository.postgres_objects import Base, Snippet


@pytest.fixture(scope="session")
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration["POSTGRES_USER"],
        app_configuration["POSTGRES_PASSWORD"],
        app_configuration["POSTGRES_HOSTNAME"],
        app_configuration["POSTGRES_PORT"],
        app_configuration["APPLICATION_DB"],
    )

    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def pg_test_data():
    return [
        {
            "code": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e",
            "language": "Python",
            "title": "Replace to join",
            "description": "''.join(data)",
            "created_at": "2021-11-13",
        },
        {
            "code": "832b1bed-d4c1-4365-9397-1ba680f309a7",
            "language": "Bash",
            "title": "Commands Docker",
            "description": "sudo service docker start",
            "created_at": "2021-11-12",
        },
        {
            "code": "4119a868-2a1d-414b-9871-a3669aabd0a0",
            "language": "Python",
            "title": "Code Pythonics",
            "description": "if data in datas: print(data)",
            "created_at": "2021-11-12",
        },
        {
            "code": "b1d70ad2-717c-4e01-b550-ae9af9c5cdac",
            "language": "Python",
            "title": "Code Pythonics",
            "description": "for data in datas: print(data)",
            "created_at": "2021-11-11",
        },
    ]


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_test_data):
    for r in pg_test_data:
        new_snippet = Snippet(
            code=r["code"],
            language=r["language"],
            title=r["title"],
            description=r["description"],
            created_at=r["created_at"],
        )
        pg_session_empty.add(new_snippet)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(Snippet).delete()
