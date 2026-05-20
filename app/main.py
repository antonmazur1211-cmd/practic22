from fastapi import FastAPI
from app.api.routes import users_router, categories_router, products_router, orders_router
from app.api.routes.auth import router as auth_router
from app.api.routes.protected import router as protected_router
from app.core.database import engine, Base

app = FastAPI(
    title="Antonmazur API with JWT Authentication",
    description="API з аутентифікацією JWT, хешуванням паролів та захищеними ендпоінтами",
    version="3.0.0"
)

# Підключення роутерів
app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

@app.get("/")
async def root():
    return {
        "message": "Лабораторна робота №5",
        "project": "Antonmazur FastAPI with JWT Authentication",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login", 
                "logout": "POST /auth/logout",
                "me": "GET /auth/me",
                "change-password": "POST /auth/change-password"
            },
            "protected": {
                "profile": "GET /protected/profile",
                "my-orders": "GET /protected/my-orders",
                "favorites": "GET /protected/favorites"
            },
            "public": {
                "users": "/users",
                "products": "/products",
                "docs": "/docs"
            }
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "auth": "JWT enabled"}
