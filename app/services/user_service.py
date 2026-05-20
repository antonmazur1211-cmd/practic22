from typing import List, Optional, Dict
from datetime import datetime
from app.models.user import UserCreate, UserUpdate, UserResponse

class UserService:
    """Сервіс для роботи з користувачами (емуляція БД через словник)"""
    
    def __init__(self):
        # Емуляція бази даних: словник {id: user_data}
        self._users: Dict[int, dict] = {}
        self._counter: int = 1
    
    def _get_next_id(self) -> int:
        """Отримати наступний ID"""
        current_id = self._counter
        self._counter += 1
        return current_id
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Створити нового користувача"""
        user_id = self._get_next_id()
        now = datetime.now()
        
        user_dict = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "age": user_data.age,
            "created_at": now,
            "updated_at": None
        }
        
        self._users[user_id] = user_dict
        return UserResponse(**user_dict)
    
    def get_all_users(self) -> List[UserResponse]:
        """Отримати всіх користувачів"""
        return [UserResponse(**user) for user in self._users.values()]
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Отримати користувача за ID"""
        user = self._users.get(user_id)
        if user:
            return UserResponse(**user)
        return None
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Оновити користувача"""
        user = self._users.get(user_id)
        if not user:
            return None
        
        # Оновлюємо тільки надані поля
        update_data = user_data.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            if value is not None:
                user[key] = value
        
        user["updated_at"] = datetime.now()
        self._users[user_id] = user
        
        return UserResponse(**user)
    
    def delete_user(self, user_id: int) -> bool:
        """Видалити користувача"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    def get_users_count(self) -> int:
        """Отримати кількість користувачів"""
        return len(self._users)

# Глобальний екземпляр сервісу
user_service = UserService()
