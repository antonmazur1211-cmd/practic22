from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    price_at_time: float = Field(..., gt=0)

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    price_at_time: float
    product: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    shipping_address: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    total_amount: float
    status: str
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
