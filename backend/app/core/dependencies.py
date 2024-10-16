from typing import Generator, List
from app.config.session import SessionLocal

from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import ALGORITHM
from app.config.settings import settings

from app.models.users import User
from app.models.roles import Role
from app.models.groups import Group
from app.crud.user import user as user_db
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError
from app.schemas.token import TokenPayload

from .security import OAuth2PasswordBearerWithCookie

reuseable_oauth = OAuth2PasswordBearerWithCookie(
    tokenUrl="/login/access-token"
)


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )

        token_data = TokenPayload(**payload)

    except jwt.JWTError as jwt_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"JWT Error: {str(jwt_error)}"
        )

    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Validation Error: {str(validation_error)}"
        )

    user = user_db.get(db, id=token_data.sub)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User detail not found')

    return user


class PermissionChecker:
    def __init__(self, permissions_required: List[Union[Role, Group]]):
        self.permissions_required = permissions_required

    def get_all_roles(self, user: User):
        permissions = set()
        for role in user.roles:
            permissions.add(role)

        for group in user.groups:
            for role in group.roles:
                permissions.add(role)
        return list(permissions)

    def __call__(self, user: User = Depends(get_current_user)):
        if user.is_superuser:
            return user

        if not user.groups and not user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this resource")

        all_roles = self.get_all_roles(user)

        for permission_required in self.permissions_required:
            # if isinstance(permission_required, Group):  # Check if it's an instance of Group and check name
            #     if permission_required.name not in [group.name for group in user_groups]:
            #         raise HTTPException(
            #             status_code=status.HTTP_403_FORBIDDEN,
            #             detail=f"Not enough permissions to access this resource.")
            # check the  roles, and check if the group contains the role required

            if permission_required.name in [role.name for role in all_roles]:
                return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this resource")


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user
