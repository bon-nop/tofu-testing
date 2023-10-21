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

