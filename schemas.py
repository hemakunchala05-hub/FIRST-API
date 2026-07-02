from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
