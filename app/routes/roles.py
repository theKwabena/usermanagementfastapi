from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas.permissions import RoleCreate, RoleResponse

from app.core.dependencies import get_db
from app.crud.permissions import role

router = APIRouter(tags=["Admin - Roles"], prefix="/admin/roles")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[RoleResponse])
def get_all_roles(database: Session = Depends(get_db)):
    return role.get_multi(db=database)


@router.get("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def get_role_by_id(role_id: int, database: Session = Depends(get_db)):
    return role.get(db=database, id=role_id)


@router.post("/", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def create_role(data: RoleCreate, database: Session = Depends(get_db)):
    new_role = role.create(
        db=database, obj_in=data
    )
    return new_role


@router.delete("/{role_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, database: Session = Depends(get_db)):
    return role.remove(db=database, id=role_id)
