# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional, Union

# class UserBase(BaseModel):
#     email: EmailStr

# class UserCreate(UserBase):
#     password: str

# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None
#     is_active: Optional[bool] = None
#     is_admin: Optional[bool] = None

# class User(UserBase):
#     id: int
#     is_active: bool
#     is_admin: bool
#     created_at: datetime
    
#     class Config:
#         from_attributes = True  # Changed from orm_mode=True for Pydantic v2

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     id: Optional[str] = None



from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

# class UserLogin(BaseModel):  # This was missing
#     email: EmailStr
#     password: 


class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None