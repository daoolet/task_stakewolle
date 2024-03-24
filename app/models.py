from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Session

from datetime import date

from .database import Base
from .schemas import UserCreate


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    referral_code = Column(String, unique=True)
    ref_code_is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=date.today)
    expiry_date = Column(DateTime)


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    referral_code = Column(String, unique=True)


class UserRepo:
    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
    
    def get_by_email(self, db: Session, user_email: str):
        return db.query(User).filter(User.email == user_email).first()
    
    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    def save_user(self, db: Session, user: UserCreate):
        new_user = User(email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user