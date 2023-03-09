from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Query
from sqlalchemy.exc import DatabaseError


class DbConfig:
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    DB_NAME = (
        config("POSTGRES_DB", default=None)
        if config("POSTGRES_DB", default=None)
        else "distvdo"
    )


engine = create_engine(DbConfig.SQLALCHEMY_DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)
session = scoped_session(Session)


class Base:
    def save(self):
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        session.delete(self)
        self._flush()

    def _flush(self):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise

    @classmethod
    def query(self) -> Query:
        return session.query(self)


Base = declarative_base(cls=Base)
