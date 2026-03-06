from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
from dataclasses import dataclass
from config import DB_NAME

Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@dataclass
class GameResult:
    score: int
    accuracy: float
    errors: int
    time: float
    rank: str
    difficulty: str
    text_title: str
    characters: int
