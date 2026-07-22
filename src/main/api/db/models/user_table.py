from sqlalchemy import Column, DateTime, Integer, String

from src.main.api.db.base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Account(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance})>"
