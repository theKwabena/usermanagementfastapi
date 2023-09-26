import os
import secrets
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException, status
from fastapi import status
from typing import Optional
from typing import Dict
from PIL import Image


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")  # changed to accept access token from httpOnly Cookie
        print("access_token is", authorization)

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


static = 'static'


async def save_picture(file, folder_name: str = '', file_name: str = None):
    random_str = secrets.token_hex(4)
    _, f_ext = os.path.splitext(file.filename)
    print(f_ext)

    if f_ext.lower() not in [".png", ".jpg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="uploaded file is not a valid image")

    # try:
    #     check_img = Image.open(file.file)
    #     print("verifying")
    #     check_img.verify()
    #     print("verifying")
    #     check_img.close()
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"There was an error verifying the uploaded image {e}")

    picture_name = str(file_name.lower()) + random_str + f_ext

    path = os.path.join(static, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)

    picture_path = os.path.join(path, picture_name)

    # output_size = (1000, 1000)
    img = Image.open(file.file)

    # img.thumbnail(output_size)
    img.save(picture_path)

    return f'{static}/{folder_name}/{picture_name}'
