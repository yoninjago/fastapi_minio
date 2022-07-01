from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database.database import get_session
from ..database.models import Base
from ..app import app

DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session
