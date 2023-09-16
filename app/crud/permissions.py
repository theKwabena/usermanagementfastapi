from uuid import UUID
from fastapi import HTTPException, status
from app.crud.base import CRUDBase

from app.schemas.permissions import Group as GroupSchema, Role as RoleSchema
from sqlalchemy.orm import Session

from app.models.groups import Group
from app.models.roles import Role
from .user import user


def check_existance(data, res_status, message):
    if not data:
        raise HTTPException(status_code=res_status, detail=message)





class RoleCrud(CRUDBase[Role, RoleSchema, RoleSchema]):
    def get_role_by_name(self, db : Session, name:str):
        return db.query(self.model).filter(self.model.name == name).first()
    def assign_role_to_user(self, db: Session, *, role_id: int, user_id: UUID):
        role = self.get(db, role_id)
        user_in_db = user.get(db=db, id=user_id)

        for user_role in user_in_db.roles:
            if user_role.id == role.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exist for user")

        user_in_db.roles.append(role)
        db.commit()
        db.refresh(user_in_db)
        return user_in_db

    def remove_role_from_user(self, db: Session, *, role_id: int, user_id: UUID):
        role = self.get(db, role_id)
        user_in_db = user.get(db, user_id)
        for user_role in user_in_db.roles:
            if user_role.id == role.id:
                user_in_db.roles.remove(role)
                db.commit()
                db.refresh(user_in_db)
                return user_in_db
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role does not exist for user")


role = RoleCrud(Role)


class GroupCrud(CRUDBase[Group, GroupSchema, GroupSchema]):
    def get_group_by_name(self, db:Session,  name : str):
        return db.query(self.model).filter(self.model.name == name).first()
    def check_group_existence(self, db:Session, *, group_id:int):
        group = self.get(db, group_id)
        check_existance(group, status.HTTP_400_BAD_REQUEST, f"Groupp with id {group_id} does not exist")
        return group
    def add_role_to_group(self, db: Session, *, group_id: int, role_id: int):
        group = self.get(db, group_id)
        role_in_db = role.get(db, role_id)
        for group_role in group.roles:
            if group_role.id == role_in_db.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exist in group")

        group.roles.append(role_in_db)
        db.commit()
        db.refresh(group)
        return group

    def remove_role_from_group(self, db: Session, *, group_id: int, role_id: int):
        group = self.get(db, group_id)
        role_in_db = role.get(db, role_id)
        for group_role in group.roles:
            if group_role.id == role_in_db.id:
                group.roles.remove(role_in_db)
                db.commit()
                db.refresh(group)
                return group
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role does not exist in group")

    def add_user_to_group(self,db: Session, *, group_id : int, user_id : UUID):
        group = self.get(db, group_id)
        check_existance(group, status.HTTP_400_BAD_REQUEST, f"Group with id {group_id} does not exist")

        user_in_db = user.get(db, user_id)
        for user_group in user_in_db.groups:
            if user_group.id == group_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User aready in group")

        user_in_db.groups.append(group)
        db.commit()
        db.refresh(user_in_db)
        return user_in_db

    def remove_user_from_group(self, db: Session, *, group_id : int, user_id : UUID):
        group = self.check_group_existence(db=db,group_id=group_id)

        user_in_db = user.get(db, user_id)
        for user_role in user_in_db.groups:
            if user_role.id == group.id:
                user_in_db.groups.remove(group)
                db.commit()
                db.refresh(user_in_db)
                return user_in_db
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not  not exist in group")



group = GroupCrud(Group)