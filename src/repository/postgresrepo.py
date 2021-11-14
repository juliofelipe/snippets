from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain import snippet
from src.repository.postgres_objects import Base, Snippet


class PostgresRepo:
    def __init__(self, configuration):
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            configuration["POSTGRES_USER"],
            configuration["POSTGRES_PASSWORD"],
            configuration["POSTGRES_HOSTNAME"],
            configuration["POSTGRES_PORT"],
            configuration["APPLICATION_DB"],
        )

        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def _create_snippet_objects(self, results):
        return [
            snippet.Snippet(
                code=q.code,
                language=q.language,
                title=q.title,
                description=q.description,
                created_at=q.created_at,
            )
            for q in results
        ]

    def list(self, filters=None):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()

        query = session.query(Snippet)

        if filters is None:
            return self._create_snippet_objects(query.all())

        if "code__eq" in filters:
            query = query.filter(Snippet.code == filters["code__eq"])

        if "language__eq" in filters:
            query = query.filter(Snippet.language == filters["language__eq"])

        if "title__eq" in filters:
            query = query.filter(Snippet.title == filters["title__eq"])

        return self._create_snippet_objects(query.all())
