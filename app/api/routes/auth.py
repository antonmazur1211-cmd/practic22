from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.database import get_db
from app.core.security import (
    create_access_token, create_refresh_token, 
    set_token_cookie, clear_token_cookie,
    get_password_hash, verify_password
)
from app.core.config import settings
from app.crud.user import crud_user
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserInfoResponse, PasswordChange
from app.core.dependencies import get_current_user
from app.core.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserInfoResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Реєстрація нового користувача"""
    existing = await crud_user.get_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Користувач з таким email вже існує")
    
    # Хешування пароля
    hashed_password = get_password_hash(user_data.password)
    
    # Створення користувача
    from app.core.models import User
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        password_hash=hashed_password,
        is_active=True,
        is_superuser=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserInfoResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        is_active=new_user.is_active,
        is_superuser=new_user.is_superuser
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Вхід в систему"""
    user = await crud_user.get_by_email(db, login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Невірний email або пароль")
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    set_token_cookie(response, access_token)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    """Вихід з системи"""
    clear_token_cookie(response)
    return {"message": "Успішний вихід"}

@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Отримання інформації про поточного користувача"""
    return UserInfoResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser
    )

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Зміна пароля"""
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Невірний старий пароль")
    
    current_user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()
    
    return {"message": "Пароль успішно змінено"}
