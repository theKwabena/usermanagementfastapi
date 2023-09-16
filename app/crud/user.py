from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate

from app.core.security import get_hashed_password,verify_password


class UserRepo(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db:Session, *, email : str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email==email).first()

    def authenticate(self, db: Session, *, email : str, password : str) -> Optional[User]:
        user_in_db = self.get_by_email(db, email=email)
        if not user_in_db:
            return None
        if not verify_password(password, user_in_db.password):
            return None
        return user_in_db

    def check_email(self, db: Session, *, user_email: str):
        user_in_db = db.query(User).filter(User.email == user_email).first()

        if user_in_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email exists")

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_hashed_password(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = UserRepo(User)
