import httpx
from fastapi import HTTPException, status
from app.api.model.user import User

# Конфигурация для обращения к микросервису
USER_SERVICE_URL = "http://0.0.0.0:8000"


async def get_current_user(token: str) -> User:
    try:
        # Отправляем запрос к микросервису с токеном
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=f"http://0.0.0.0:8080/api/v1/auth/user",
                headers={"Authorization": f"Bearer {token}"}
            )

        # Проверяем статус ответа
        if response.status_code != 200: raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

        # Десериализуем данные пользователя
        user_data = response.json()

        # Возвращаем пользователя
        return User(**user_data)

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user data: {str(e)}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while connecting to the user service: {str(e)}"
        )
