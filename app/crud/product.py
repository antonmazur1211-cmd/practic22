from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud.base import CRUDBase

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    async def get_by_category(self, db: AsyncSession, category_id: int) -> list[Product]:
        result = await db.execute(select(Product).where(Product.category_id == category_id))
        return result.scalars().all()
    
    async def get_available(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product).where(Product.is_available == True))
        return result.scalars().all()

crud_product = CRUDProduct(Product)
