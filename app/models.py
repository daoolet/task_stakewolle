from sqlalchemy import Column, Integer, String, DateTime, Boolean

from datetime import date

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    referral_code = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=date.today)
    expiry_date = Column(DateTime)


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    referral_code = Column(String, unique=True)


