from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, PermissionChecker
from app.schemas.permissions import GroupCreate, GroupResponse
from app.crud.permissions import group

from .base import  admin
router = APIRouter(tags=["Admin - Groups"], prefix="/admin/groups")# dependencies=[Depends(PermissionChecker([admin]))])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GroupResponse])
def get_groups(database: Session = Depends(get_db)):
    return group.get_multi(db=database)


@router.get("/{group_id}", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def get_group_by_id(group_id: int, database: Session = Depends(get_db)):
    return group.get(db=database, id=group_id)


@router.post("/", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def create_group(data: GroupCreate, database: Session = Depends(get_db)):
    check_group_name = group.get_group_by_name(db=database, name=data.name)
    if check_group_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Group with name {check_group_name.name} already exist ")
    new_group = group.create(
        db=database, obj_in=data
    )
    return new_group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, database: Session = Depends(get_db)):
    return group.remove(db=database, id=group_id)


@router.post("/{group_id}/roles", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def add_role_to_group(group_id: int, role_id: int, database: Session = Depends(get_db)):
    return group.add_role_to_group(db=database, group_id=group_id, role_id=role_id)


@router.delete("/{group_id}/roles", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def remove_role_from_group(group_id: int, role_id: int, database: Session = Depends(get_db)):
    return group.remove_role_from_group(db=database, group_id=group_id, role_id=role_id)

@router.put("/{group_id}", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def edit_group(group_id : int, group_in: GroupCreate, database : Session=Depends((get_db))):
    group_in_db = group.get(db=database, id=group_id)
    if not group_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="group not found"
        )

    check_name = group.get_group_by_name(db=database,name=group_in.name)
    if not check_name.name == group_in_db.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Group with name {group_in.name} exists'
        )
    return group.update(db=database, db_obj=group_in_db, obj_in=group_in)