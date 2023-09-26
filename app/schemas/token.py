from typing import Optional

from pydantic import BaseModel
from .user import CurrentUserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

class SignInResponse(BaseModel):
    user : CurrentUserResponse


class TokenPayload(BaseModel):
    sub: Optional[str] = None
