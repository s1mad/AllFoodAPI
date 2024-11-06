from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from typing import Optional

# Конфигурация OAuth2 для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenRequest(BaseModel):
    token: str


# Модель пользователя для проверки прав
class User(BaseModel):
    id: int
    username: str
    is_owner: bool


# Секретный ключ для декодирования JWT (здесь упрощённо, лучше брать из переменных окружения)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# Функция для получения текущего пользователя
async def get_current_user(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        username: str = payload.get("username")
        is_owner: bool = payload.get("is_owner")

        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if not is_owner:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not an owner")

        return User(id=user_id, username=username, is_owner=is_owner)

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")