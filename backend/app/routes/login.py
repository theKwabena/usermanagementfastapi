from datetime import timedelta
from fastapi import APIRouter, Depends, Response, File, UploadFile, BackgroundTasks, status, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from app.core.security import create_access_token, generate_user_token, verify_user_token, get_hashed_password
from app.core.dependencies import get_db, get_current_active_user
from app.crud.user import user
from app.models.users import User
# from app.core.dependencies import get_current_active_user
from app.config.settings import settings
from app.schemas.token import SignInResponse, RequestToken
from app.schemas.user import (
    CurrentUserResponse, UserCreate,
    SignUpResponse, UserUpdate,
    ResetPassword, UserResetPassword, UserChangePassword)
from app.utils.images import save_picture
from app.utils.appmails import send_email

router = APIRouter(tags=['Profile'])


@router.post('/sign-up', response_model=SignUpResponse, )
async def sign_up(data: UserCreate, background_tasks: BackgroundTasks, database: Session = Depends(get_db)):
    user.check_email(db=database, user_email=data.email)
    new_user = user.create(
        db=database, obj_in=data
    )
    email_token = generate_user_token(new_user.email)
    await send_email(
        background_tasks,
        f"Welcome to {settings.PROJECT_NAME}",
        new_user.email,
        {
            "project_name": settings.PROJECT_NAME,
            "link": f"{settings.FRONTEND_HOST_URL}verify-email/{email_token}/"
        },
        'new_account.html'
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
                        httponly=True)
    return {
        "user": user_in_db
    }


@router.post('/', response_model=CurrentUserResponse, status_code=status.HTTP_200_OK)
async def update_profile_picture(file: UploadFile = File(...),
                                 database: Session = Depends(get_db),
                                 user_in: User = Depends(get_current_active_user)):
    image_url = await save_picture(file, 'users', file_name=f'{user_in.first_name}{user_in.last_name}')
    return user.save_profile_picture(db=database, image_url=image_url, user_in=user_in)


@router.post('/verify-email/', response_model=CurrentUserResponse, status_code=status.HTTP_200_OK)
def verify_user_email(data: RequestToken, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    user_email = verify_user_token(data.token)
    if not user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide an email")
    if not user_email == current_user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The email provided does not match user's email")
    user.verify_email(db=db, user_in=current_user)
    return current_user


@router.post('/password-recovery/', status_code=status.HTTP_200_OK)
async def send_password_token(
        data: ResetPassword, background_tasks: BackgroundTasks, database: Session = Depends(get_db)
) -> Any:
    user_in_db = user.get_by_email(db=database, email=data.email)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no account associated with the email provided"
        )
    email_token = generate_user_token(user_in_db.email)
    await send_email(
        background_tasks,
        "Password Reset Request",
        user_in_db.email,
        {
            "username": user_in_db.first_name,
            "project_name": settings.PROJECT_NAME,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "link": f"{settings.FRONTEND_HOST_URL}reset-password/{email_token}/"
        },
        'reset_password.html'
    )
    return {'status': 'Success'}


@router.put("/reset-password/", status_code=status.HTTP_200_OK)
def reset_password(data: UserResetPassword, db: Session = Depends(get_db)) -> Any:
    email = verify_user_token(data.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user_in_db = user.get_by_email(db=db, email=email)
    if not user_in_db:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    hashed_password = get_hashed_password(data.new_password)
    user_in_db.password = hashed_password
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    return {'status': 'success'}


@router.put("/change-password/", status_code=status.HTTP_200_OK)
def change_password(
        data: UserChangePassword, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    user.authenticate(db=db, email=current_user.email, password=data.old_password)

    hashed_password = get_hashed_password(data.new_password)
    current_user.password = hashed_password
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {'status': 'success'}


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {'status': 'success'}


@router.get('/profile', response_model=CurrentUserResponse)
def get_current_user(
        user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    return user


@router.delete('/profile', status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return user.remove(db=db, id=current_user.id)


@router.put('/profile', response_model=CurrentUserResponse)
def update_current_user(
        user_update: UserUpdate,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return user.update(db=db, db_obj=current_user, obj_in=user_update)
