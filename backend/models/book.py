from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from db.session import Base


class Book(Base):
    __tablename__ = "books"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)