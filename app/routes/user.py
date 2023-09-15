from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, PermissionChecker, admin_create_role
from app.crud.user import user
from app.crud.permissions import role, group

from app.models.users import User
from app.schemas.user import UserResponse, UserCreate

from .base import admin, admin_can_create

router = APIRouter(tags=["User"], prefix="/users")

@router.get("/", status_code=status.HTTP_200_OK,
            dependencies=[Depends(PermissionChecker([admin, admin_can_create]))],
            response_model=list[UserResponse])
def users(database: Session = Depends(get_db)):
    return user.get_multi(db=database, skip=0, limit=10)


@router.post("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def create_user(data: UserCreate, database: Session = Depends(get_db)):
    # Check if user with email exists
    check_user = user.check_email(db=database, user_email=data.email)
    new_data = user.create(
        db=database, obj_in=data
    )
    return new_data


@router.get("/{user_id}",
            status_code=status.HTTP_200_OK,
            response_model=UserResponse,
            dependencies = [Depends(PermissionChecker([admin_create_role]))]
            )
def get_user_by_id(user_id: UUID,    current_user: Annotated[User, Depends(get_current_user)], database: Session = Depends(get_db)):
    return user.get(id=user_id, db=database)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, database: Session = Depends(get_db)):
    return user.remove(db=database, id=user_id)


@router.post("/{user_id}/roles", status_code=status.HTTP_200_OK)
def assign_role_to_user(user_id: UUID, role_id: int, database: Session = Depends(get_db)):
    return role.assign_role_to_user(db=database, role_id=role_id, user_id=user_id)


@router.delete("/{user_id}/roles", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_user(user_id: UUID, role_id: int, database: Session = Depends(get_db)):
    return role.remove_role_from_user(db=database, role_id=role_id, user_id=user_id)


@router.post("{user_id}/groups", status_code=status.HTTP_200_OK)
def add_user_to_group(user_id: UUID, group_id: int, database: Session = Depends(get_db)):
    return group.add_user_to_group(db=database, group_id=group_id, user_id=user_id)


@router.delete("{user_id}/groups", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_from_group(user_id: UUID, group_id: int, database: Session = Depends(get_db)):
    return group.remove_user_from_group(db=database, group_id=group_id, user_id=user_id)
