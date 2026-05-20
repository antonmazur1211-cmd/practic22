from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate, UserProfileCreate
from app.crud.base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_with_profile(self, db: AsyncSession, user_in: UserCreate, profile_in: UserProfileCreate | None = None) -> User:
        user = await self.create(db, user_in)
        if profile_in:
            profile = UserProfile(**profile_in.model_dump(), user_id=user.id)
            db.add(profile)
            await db.flush()
        return user

crud_user = CRUDUser(User)
