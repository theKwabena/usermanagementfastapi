from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, PermissionChecker
from app.crud.user import user
from app.crud.permissions import role, group

from pydantic import EmailStr
from app.models.users import User
from app.schemas.user import UserResponse, UserCreate, UserRoleResponse, UserGroupResponse, UserUpdate

from .base import admin, admin_create, admin_edit, admin_delete, admin_list

router = APIRouter(tags=["User"], prefix="/users")


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=list[UserResponse],
            # dependencies=[Depends(PermissionChecker([admin_list, admin_edit, admin_delete, admin_create]))]
            )
def users(database: Session = Depends(get_db)):
    return user.get_multi(db=database, skip=0, limit=10)


@router.post("/", status_code=status.HTTP_200_OK,
             response_model=UserResponse,
             dependencies=[Depends(PermissionChecker([admin_create]))]
             )
def create_user(data: UserCreate, database: Session = Depends(get_db)):
    # Check if user with email exists
    user.check_email(db=database, user_email=data.email)
    new_data = user.create(
        db=database, obj_in=data
    )
    return new_data


@router.get("/{user_id}",
            status_code=status.HTTP_200_OK,
            response_model=UserResponse,
            dependencies=[Depends(PermissionChecker([admin_list, admin_edit, admin_delete, admin_create]))]
            )
def get_user_by_id(user_id: UUID, database: Session = Depends(get_db)):
    return user.get(id=user_id, db=database)


# @router.get('', status_code=status.HTTP_200_OK)
# def get_user_by_email(user_email: EmailStr, database:Session = Depends(get_db)):
#     return user.get_by_email(db=database, email=user_email)
@router.delete("/{user_id}",
               dependencies=[Depends(PermissionChecker([admin_delete]))],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, database: Session = Depends(get_db)):
    return user.remove(db=database, id=user_id)


@router.put("/{user_id}",
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(PermissionChecker([admin_edit]))],
            response_model=UserResponse)
def update_user(user_id: UUID, user_in: UserUpdate, database: Session = Depends(get_db)):
    user_in_db = user.get(db=database, id=user_id)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user.update(db=database, db_obj=user_in_db, obj_in=user_in)


@router.post("/{user_id}/roles",
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(PermissionChecker([]))],
             response_model=UserRoleResponse)
def assign_role_to_user(user_id: UUID, role_id: int, database: Session = Depends(get_db)):
    return role.assign_role_to_user(db=database, role_id=role_id, user_id=user_id)


@router.delete("/{user_id}/roles",
               status_code=status.HTTP_200_OK,
               dependencies=[Depends(PermissionChecker([]))],
               response_model=UserRoleResponse)
def remove_role_from_user(user_id: UUID, role_id: int, database: Session = Depends(get_db)):
    return role.remove_role_from_user(db=database, role_id=role_id, user_id=user_id)


@router.post("/{user_id}/groups",
             status_code=status.HTTP_200_OK,
             dependencies=[Depends(PermissionChecker([]))],
             response_model=UserGroupResponse)
def add_user_to_group(user_id: UUID, group_id: int, database: Session = Depends(get_db)):
    return group.add_user_to_group(db=database, group_id=group_id, user_id=user_id)


@router.delete("/{user_id}/groups",
               dependencies=[Depends(PermissionChecker([]))],
               status_code=status.HTTP_200_OK,
               response_model=UserGroupResponse)
def remove_user_from_group(user_id: UUID, group_id: int, database: Session = Depends(get_db)):
    return group.remove_user_from_group(db=database, group_id=group_id, user_id=user_id)
