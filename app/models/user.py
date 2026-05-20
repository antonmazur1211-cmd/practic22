from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Базова схема користувача"""
    name: str = Field(..., min_length=2, max_length=50, description="Ім'я користувача")
    email: EmailStr = Field(..., description="Email користувача")
    age: Optional[int] = Field(None, ge=0, le=150, description="Вік користувача")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Ім\'я не може бути порожнім')
        return v.title()

class UserCreate(UserBase):
    """Схема для створення користувача"""
    pass

class UserUpdate(BaseModel):
    """Схема для оновлення користувача (всі поля опціональні)"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(UserBase):
    """Схема для відповіді API"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
