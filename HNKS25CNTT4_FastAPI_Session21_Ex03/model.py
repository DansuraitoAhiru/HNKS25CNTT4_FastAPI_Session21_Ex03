from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), default="student",nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)