from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_token, get_token_from_cookie
from app.crud.user import crud_user
from app.core.models import User

# Схема для Bearer токена (альтернатива кукі)
security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> User:
    """Отримання поточного аутентифікованого користувача"""
    token = None
    
    # Спроба отримати токен з Authorization header
    if credentials:
        token = credentials.credentials
    
    # Якщо немає в header, спробувати з кукі
    if not token:
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не надано токен аутентифікації",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Декодування токена
    payload = decode_token(token)
    
    # Перевірка типу токена
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недійсний тип токена",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не знайдено ID користувача в токені",
        )
    
    # Отримання користувача з БД
    user = await crud_user.get(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Користувача деактивовано",
        )
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Отримання активного користувача"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивний користувач")
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Отримання суперкористувача (адміністратора)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостатньо прав",
        )
    return current_user
