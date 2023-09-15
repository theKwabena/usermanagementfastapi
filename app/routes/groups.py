from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.permissions import GroupCreate, GroupResponse
from app.crud.permissions import group

router = APIRouter(tags=["Admin - Groups"], prefix="/admin/groups")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[GroupResponse])
def get_groups(database: Session = Depends(get_db)):
    return group.get_multi(db=database)


@router.get("/{group_id}", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def get_group_by_id(group_id: int, databse: Session = Depends(get_db)):
    return group.get(db=databse, id=group_id)


@router.post("/", status_code=status.HTTP_200_OK, response_model=GroupResponse)
def create_group(data: GroupCreate, database: Session = Depends(get_db)):
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


@router.delete("/{group_id}/roles", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_group(group_id: int, role_id: int, database: Session = Depends(get_db)):
    return group.remove_role_from_group(db=database, group_id=group_id, role_id=role_id)
