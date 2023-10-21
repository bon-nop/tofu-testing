from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    address = Column(String)
    expect_salary = Column(Integer)

class Queue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    wh_id = Column(Integer)
    door = Column(Integer)
    vehicle_types = Column(Integer)
    vehicle_license = Column(String)
    start_load_time = Column(DateTime)
    finish_load_time = Column(DateTime)
    status = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(DateTime)

class Warehouse(Base):
    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, index=True)
    wh_name = Column(String)
    door_1 = Column(Integer)
    door_2 = Column(Integer)
    door_3 = Column(Integer)
    door_4 = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(DateTime)
