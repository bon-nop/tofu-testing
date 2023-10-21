from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    address: str | None = None
    expect_salary: int | None = None


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: int


class QueueBase(BaseModel):
    wh_id: int
    door: int | None = None
    vehicle_types: int
    vehicle_license: str | None = None
    start_load_time: str | None = None
    finish_load_time: str | None = None
    status: int
    created_at: str | None = None
    updated_at: str | None = None


class QueueCreate(QueueBase):
    pass


class Queue(QueueBase):
    id: int


class WarehouseBase(BaseModel):
    wh_name: str
    door_1: int | None = None
    door_2: int | None = None
    door_3: int | None = None
    door_4: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int
