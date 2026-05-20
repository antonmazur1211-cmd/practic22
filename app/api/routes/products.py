from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.crud import crud_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud_product.create(db, product_in)

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0, 
    limit: int = 100,
    available: Optional[bool] = Query(None),
    category_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    if available:
        return await crud_product.get_available(db)
    if category_id:
        return await crud_product.get_by_category(db, category_id)
    return await crud_product.get_multi(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await crud_product.update(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_product.delete(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
