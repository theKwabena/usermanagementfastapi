from uuid import UUID
from typing import List, Union, Optional

from pydantic import BaseModel, constr, EmailStr, FileUrl
from enum import Enum

from .permissions import Role, Group, GroupResponse, RoleResponse


class UserBase(BaseModel):
    id: UUID


class UserCreate(BaseModel):
    first_name: constr(min_length=2, max_length=255)
    last_name: constr(min_length=2, max_length=2555)
    email: EmailStr
    phone_number: Optional[str] = None
    password: str

    is_superuser: Optional[bool] = False
    email_verified: Optional[bool] = False
    auth_identity_provider: Optional[str] = None


class SignUpResponse(UserCreate):
    pass


class UserResponse(UserBase):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    roles: list[RoleResponse]
    groups: list[GroupResponse]
    profile_img: Optional[str]

    class Config:
        from_attributes = True


class UserRoleResponse(UserBase):
    roles: list[Role]

    class Config:
        from_attributes = True


class UserGroupResponse(UserBase):
    groups: list[Group]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[constr(min_length=2, max_length=255)] = None
    last_name: Optional[constr(min_length=2, max_length=255)] = None
    phone_number: Optional[str] = None


class CurrentUserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    roles: list[RoleResponse]
    groups: list[GroupResponse]
    profile_img: Optional[str]
    is_superuser: Optional[bool]

    class Config:
        from_attributes = True
