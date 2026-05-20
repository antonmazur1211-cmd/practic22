from .users import router as users_router
from .categories import router as categories_router
from .products import router as products_router
from .orders import router as orders_router
from .auth import router as auth_router
from .protected import router as protected_router

__all__ = [
    "users_router",
    "categories_router", 
    "products_router",
    "orders_router",
    "auth_router",
    "protected_router"
]
