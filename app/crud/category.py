from app.core.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass

crud_category = CRUDCategory(Category)
