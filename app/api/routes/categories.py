from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.crud import crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(cat_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud_category.create(db, cat_in)

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud_category.get_multi(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await crud_category.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, cat_in: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    category = await crud_category.update(db, category_id, cat_in)
    if not category:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_category.delete(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")
