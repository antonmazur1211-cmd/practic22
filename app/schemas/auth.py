from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserRegister(BaseModel):
    """Схема для реєстрації"""
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль повинен містити мінімум 6 символів')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль повинен містити хоча б одну цифру')
        if not any(c.isalpha() for c in v):
            raise ValueError('Пароль повинен містити хоча б одну літеру')
        return v

class UserLogin(BaseModel):
    """Схема для логіну"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Відповідь з токеном"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserInfoResponse(BaseModel):
    """Інформація про користувача для відповіді"""
    id: int
    name: str
    email: str
    is_active: bool
    is_superuser: bool

class PasswordChange(BaseModel):
    """Зміна пароля"""
    old_password: str
    new_password: str = Field(..., min_length=6)
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Пароль повинен містити мінімум 6 символів')
        return v
