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


class GroupCrud(CRUDBase[Group, GroupSchema, GroupSchema]):
    def get_group_by_name(self, db:Session,  name : str):
        return db.query(Group).filter(Group.name == name).first()
    def check_group_existence(self, db:Session, *, group_id:int):
        group = self.get(db, group_id)
        check_existance(group, status.HTTP_400_BAD_REQUEST, f"Groupp with id {group_id} does not exist")
        return group
    def add_role_to_group(self, db: Session, *, group_id: int, role_id: int):
        group = self.get(db, group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group with id does not exist")

        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role with id does not exist")

        for group_role in group.roles:
            if group_role.id == role.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exist in group")

        group.roles.append(role)
        db.commit()
        db.refresh(group)
        return group

    def remove_role_from_group(self, db: Session, *, group_id: int, role_id: int):
        group = self.get(db, group_id)
        check_existance(group, status.HTTP_400_BAD_REQUEST, f"Role with id {role_id} does not exits")
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role with id does not exist")

        for group_role in group.roles:
            if group_role.id == role.id:
                group.roles.remove(role)
                db.commit()
                db.refresh(group)
                return group
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role does nnot exist in group")

    def add_user_to_group(self,db: Session, *, group_id : int, user_id : UUID):
        group = self.get(db, group_id)
        check_existance(group, status.HTTP_400_BAD_REQUEST, f"Group with id {group_id} does not exist")

        user_in_db = user.get(db, user_id)
        check_existance(user_in_db, status.HTTP_400_BAD_REQUEST, f"User with id {id} does not exist")

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
        check_existance(user_in_db, status.HTTP_400_BAD_REQUEST, f"User with id {id} does not exist")

        for user_role in user_in_db.groups:
            if user_role.id == group.id:
                user_in_db.groups.remove(group)
                db.commit()
                db.refresh(user_in_db)
                return user_in_db
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not  not exist in group")



group = GroupCrud(Group)


class RoleCrud(CRUDBase[Role, RoleSchema, RoleSchema]):
    def assign_role_to_user(self, db: Session, *, role_id: int, user_id: UUID):
        role = self.get(db, role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role with id does not exist")

        user_in_db = user.get(db=db, id=user_id)
        if not user_in_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with id does not exist")


        for user_role in user_in_db.roles:
            if user_role.id == role.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exist for user")

        user_in_db.roles.append(role)
        db.commit()
        db.refresh(user_in_db)
        return user_in_db

    def remove_role_from_user(self, db: Session, *, role_id: int, user_id: UUID):
        role = self.get(db, role_id)
        check_existance(role, status.HTTP_400_BAD_REQUEST, f"Role with id {role_id} does not exist")

        user_in_db = user.get(db, user_id)
        check_existance(user_in_db, status.HTTP_400_BAD_REQUEST, f"User with id {user_id} does not exist")
        for user_role in user_in_db.roles:
            if user_role.id == role.id:
                user_in_db.roles.remove(role)
                db.commit()
                db.refresh(user_in_db)
                return user_in_db
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role does not exist in for user")


role = RoleCrud(Role)
