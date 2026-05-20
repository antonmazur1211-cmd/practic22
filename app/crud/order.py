from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate
from app.crud.base import CRUDBase

class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    async def get_by_user(self, db: AsyncSession, user_id: int) -> list[Order]:
        result = await db.execute(select(Order).where(Order.user_id == user_id))
        return result.scalars().all()
    
    async def create_with_items(self, db: AsyncSession, user_id: int, order_in: OrderCreate) -> Order:
        total = 0
        items_data = []
        for item in order_in.items:
            # Тут має бути логіка отримання ціни з продукту
            total += item.quantity * item.price_at_time
            items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_time": item.price_at_time
            })
        
        order = Order(
            user_id=user_id,
            total_amount=total,
            shipping_address=order_in.shipping_address
        )
        db.add(order)
        await db.flush()
        
        for item_data in items_data:
            order_item = OrderItem(**item_data, order_id=order.id)
            db.add(order_item)
        
        await db.flush()
        return order

crud_order = CRUDOrder(Order)
