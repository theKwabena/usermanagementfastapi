from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from app.core.security import create_access_token, create_refresh_token
from app.core.dependencies import get_db
from app.crud.user import user
from app.config.settings import settings

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user_in_db = user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_in_db.id, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(user_in_db.email, expires_delta=access_token_expires),
        "token_type" : "bearer"
    }
