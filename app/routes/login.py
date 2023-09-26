from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from app.core.security import create_access_token, create_refresh_token
from app.core.dependencies import get_db, get_current_active_user
from app.crud.user import user
from app.models.users import User
# from app.core.dependencies import get_current_active_user
from app.config.settings import settings
from app.schemas.token import SignInResponse
from app.schemas.user import UserResponse, CurrentUserResponse, UserCreate, SignUpResponse, UserUpdate
from app.core.utils import save_picture

router = APIRouter(tags=['Profile'])


@router.post('/sign-up', response_model=SignUpResponse)
def sign_up(data: UserCreate, database: Session = Depends(get_db)):
    user.check_email(db=database, user_email=data.email)
    new_user = user.create(
        db=database, obj_in=data
    )
    return new_user


@router.post("/login/access-token", response_model=SignInResponse)
def login_access_token(response: Response, db: Session = Depends(get_db),
                       form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user_in_db = user.authenticate(db, email=form_data.username, password=form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_in_db.id, expires_delta=access_token_expires)
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}",
                        samesite='lax',
                        expires=60 * 60 * 8,
                        httponly=True)  # set HttpOnly cookie in response
    return {
        # "access_token": access_token,
        # "refresh_token": create_refresh_token(user_in_db.email, expires_delta=access_token_expires),
        "user": user_in_db
    }


@router.get('/profile', response_model=CurrentUserResponse)
def get_current_user(
        user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    return user


@router.delete('/profile')
def delete_current_user(
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return user.remove(db=db, id=current_user.id)


@router.put('/profile', response_model=CurrentUserResponse)
def update_current_user(
        user_update : UserUpdate,
        current_user=Depends(get_current_active_user),
        db:Session = Depends(get_db)
):

    return user.update(db=db, db_obj=current_user, obj_in=user_update)

@router.post('/profile', response_model=CurrentUserResponse)
async def update_profile_picture(file: UploadFile = File(...),
                                 database: Session = Depends(get_db),
                                 user_in: User = Depends(get_current_active_user)):
    image_url = await save_picture(file, 'users', file_name=f'{user_in.first_name}{user_in.last_name}')
    return user.save_profile_picture(db=database, image_url=image_url, user_in=user_in)


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {'status': 'success'}
