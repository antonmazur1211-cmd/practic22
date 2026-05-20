import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.models import User
from app.core.security import get_password_hash

async def create_admin():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Перевірка чи вже існує адмін
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.email == "admin@antonmazur.com"))
        admin = result.scalar_one_or_none()
        
        if admin:
            print("Адміністратор вже існує!")
            return
        
        # Створення адміністратора
        admin = User(
            name="Admin",
            email="admin@antonmazur.com",
            password_hash=get_password_hash("admin123"),
            age=30,
            is_active=True,
            is_superuser=True
        )
        session.add(admin)
        await session.commit()
        print("✅ Адміністратора створено!")
        print("   Email: admin@antonmazur.com")
        print("   Password: admin123")

if __name__ == "__main__":
    asyncio.run(create_admin())
