from uuid import UUID
from typing import List, Union, Optional

from pydantic import BaseModel, constr, EmailStr
from enum import Enum

from .permissions import Role, Group


class UserCreate(BaseModel):
    first_name: constr(min_length=2, max_length=255)
    last_name: constr(min_length=2, max_length=2555)
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    roles: list[Role]
    groups: list[Group]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[constr(min_length=2, max_length=255) ]  = None
    last_name:Optional[constr(min_length=2, max_length=255)]  = None
    email: EmailStr
