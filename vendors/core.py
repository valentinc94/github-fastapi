from typing import Optional

from pydantic import BaseModel, Field


class Auth(BaseModel):
    token: str


class UserData(BaseModel):
    bio: Optional[str] = Field(None)
    blog: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    company: Optional[str] = Field(None)
    location: Optional[str] = Field(None)


class UserUpdate(BaseModel):
    auth: Auth
    user: UserData
