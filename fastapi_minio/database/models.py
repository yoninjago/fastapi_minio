from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MinioUploadedFiles(Base):
    __tablename__ = 'inbox'

    id = Column(Integer, primary_key=True)
    request_code = Column(Integer)
    filename = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
