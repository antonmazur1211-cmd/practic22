from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

# Секретний ключ
SECRET_KEY = "antonmazur-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Тимчасова БД в пам'яті
fake_db: Dict[int, dict] = {}
user_counter = 1

# Моделі
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    age: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Функції
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Недійсний токен")

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не знайдено ID")
    user = fake_db.get(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    return user

# FastAPI додаток
app = FastAPI(title="Antonmazur Auth Demo (без БД)")

@app.post("/auth/register", status_code=201)
async def register(user_data: UserRegister):
    global user_counter
    
    # Перевірка чи email існує
    for user in fake_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="Email вже використовується")
    
    # Створення користувача
    user_id = user_counter
    user_counter += 1
    
    fake_db[user_id] = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "age": user_data.age,
        "password_hash": get_password_hash(user_data.password)
    }
    
    return {"id": user_id, "name": user_data.name, "email": user_data.email}

@app.post("/auth/login")
async def login(login_data: UserLogin):
    # Пошук користувача
    user = None
    for u in fake_db.values():
        if u["email"] == login_data.email:
            user = u
            break
    
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Невірний email або пароль")
    
    token = create_access_token(data={"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["id"], "name": current_user["name"], "email": current_user["email"]}

@app.get("/protected/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {"message": "Це захищений профіль", "user": current_user["name"]}

@app.get("/protected/favorites")
async def get_favorites(current_user: dict = Depends(get_current_user)):
    return {"favorites": [], "user": current_user["name"]}

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "in-memory"}

@app.get("/")
async def root():
    return {
        "message": "Лабораторна робота №5 - JWT Аутентифікація",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /auth/register",
            "login": "POST /auth/login",
            "me": "GET /auth/me",
            "protected": "GET /protected/profile"
        }
    }
