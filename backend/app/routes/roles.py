from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.permissions import RoleCreate, RoleResponse

from .base import admin
from app.core.dependencies import get_db, PermissionChecker
from app.crud.permissions import role

router = APIRouter(tags=["Admin - Roles"],
                   prefix="/admin/roles", )  # dependencies=[Depends(PermissionChecker([admin]))])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RoleResponse])
def get_all_roles(database: Session = Depends(get_db)):
    return role.get_multi(db=database)


@router.get("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def get_role_by_id(role_id: int, database: Session = Depends(get_db)):
    return role.get(db=database, id=role_id)


@router.post("/", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def create_role(data: RoleCreate, database: Session = Depends(get_db)):
    check_role_name = role.get_role_by_name(db=database, name=data.name)
    if check_role_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Role with name {check_role_name.name} exists")
    new_role = role.create(
        db=database, obj_in=data
    )
    return new_role


@router.put("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def edit_role(role_id: int, role_in: RoleCreate, database: Session = Depends((get_db))):
    role_in_db = role.get(db=database, id=role_id)
    if not role_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ROle not found"
        )

    check_name = role.get_role_by_name(db=database, name=role_in.name)
    if check_name:
        if not check_name.name == role_in_db.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Role with name {role_in.name} exists'
            )
    return role.update(db=database, db_obj=role_in_db, obj_in=role_in)


@router.delete("/{role_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, database: Session = Depends(get_db)):
    return role.remove(db=database, id=role_id)
