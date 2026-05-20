from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncpg
import os
from typing import Optional

# Отримання URL бази даних з змінних середовища
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://antonmazur:password123@localhost:5432/antonmazur_db")

# Глобальний пул з'єднань
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Стартап: створення пулу з'єднань
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL)
        print("✅ Підключення до PostgreSQL встановлено")
        
        # Створення таблиці users
        async with db_pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Таблицю users перевірено/створено")
    except Exception as e:
        print(f"❌ Помилка підключення до БД: {e}")
    
    yield
    
    # Шадаун: закриття пулу
    if db_pool:
        await db_pool.close()
        print("🔌 Підключення до PostgreSQL закрито")

app = FastAPI(
    title="Antonmazur API with PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Hello from Antonmazur Docker Container!",
        "status": "running",
        "database": "PostgreSQL"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "container": "fastapi",
        "database": "connected" if db_pool else "disconnected"
    }

@app.post("/users")
async def create_user(name: str, email: str):
    """Створення нового користувача"""
    try:
        async with db_pool.acquire() as conn:
            user_id = await conn.fetchval(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
                name, email
            )
            return {"id": user_id, "name": name, "email": email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users")
async def get_users():
    """Отримання всіх користувачів"""
    try:
        async with db_pool.acquire() as conn:
            users = await conn.fetch("SELECT id, name, email, created_at FROM users")
            return [dict(user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Отримання користувача за ID"""
    try:
        async with db_pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT id, name, email, created_at FROM users WHERE id = $1",
                user_id
            )
            if user:
                return dict(user)
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/db-info")
async def db_info():
    """Інформація про базу даних"""
    try:
        async with db_pool.acquire() as conn:
            version = await conn.fetchval("SELECT version()")
            return {"database": "PostgreSQL", "version": version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
