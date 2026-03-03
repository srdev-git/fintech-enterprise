from src.infrastructure.database.models import Base
from src.infrastructure.database.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)