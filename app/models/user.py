from sqlalchemy import Column, String, func, Integer, DateTime, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    registered_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, login={self.login})>"