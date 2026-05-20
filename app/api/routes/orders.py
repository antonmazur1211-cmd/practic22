from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.crud import crud_order, crud_user
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(user_id: int, order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return await crud_order.create_with_items(db, user_id, order_in)

@router.get("/", response_model=List[OrderResponse])
async def get_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_order.get_multi(db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_orders_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_order.get_by_user(db, user_id)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await crud_order.get(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order_in: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await crud_order.update(db, order_id, order_in)
    if not order:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return order

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_order.delete(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
