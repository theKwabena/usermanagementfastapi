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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Provided email is not associated with any account")
        if not verify_password(password, user_in_db.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
        return user_in_db

    def check_email(self, db: Session, *, user_email: str):
        user_in_db = db.query(User).filter(User.email == user_email).first()
        if user_in_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with email exists")

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            phone_number = obj_in.phone_number,
            password=get_hashed_password(obj_in.password),
            is_superuser=obj_in.is_superuser,
            email_verified=obj_in.email_verified,
            auth_identity_provider = obj_in.auth_identity_provider

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def save_profile_picture(self, db : Session, *, image_url : str, user_in:User):
        user = self.get(db,user_in.id)
        user.profile_img = image_url
        db.commit()
        db.refresh(user)
        return user

    def verify_email(self, db:Session, *, user_in:User):
        user_in_db = self.get(db, user_in.id)
        user_in_db.email_verified = True
        db.commit()
        db.refresh(user_in_db)
        return user_in_db

user = UserRepo(User)
