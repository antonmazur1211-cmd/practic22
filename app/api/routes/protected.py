from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_superuser
from app.core.models import User
from app.crud import crud_product, crud_order
from app.schemas.product import ProductResponse
from app.schemas.order import OrderResponse

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Отримання профілю (тільки для авторизованих)"""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "message": "Це захищена інформація"
    }

@router.get("/my-orders")
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Отримання замовлень поточного користувача"""
    orders = await crud_order.get_by_user(db, current_user.id)
    return orders

@router.post("/favorites/{product_id}")
async def add_to_favorites(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Додавання товару до обраного"""
    product = await crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    
    if product not in current_user.favorite_products:
        current_user.favorite_products.append(product)
        await db.commit()
        return {"message": f"Товар додано до обраного"}
    return {"message": "Товар вже в обраному"}

@router.get("/favorites")
async def get_favorites(current_user: User = Depends(get_current_user)):
    """Отримання списку обраних товарів"""
    return [
        {"id": p.id, "name": p.name, "price": p.price}
        for p in current_user.favorite_products
    ]

@router.delete("/favorites/{product_id}")
async def remove_from_favorites(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Видалення товару з обраного"""
    product = await crud_product.get(db, product_id)
    if product and product in current_user.favorite_products:
        current_user.favorite_products.remove(product)
        await db.commit()
        return {"message": "Товар видалено з обраного"}
    return {"message": "Товар не знайдено в обраному"}

@router.get("/admin/users")
async def get_all_users(
    current_user: User = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """Отримання всіх користувачів (тільки адмін)"""
    from app.crud.user import crud_user
    users = await crud_user.get_multi(db)
    return [
        {"id": u.id, "name": u.name, "email": u.email, "is_active": u.is_active}
        for u in users
    ]
