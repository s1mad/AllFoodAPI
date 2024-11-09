import httpx

# Конфигурация для обращения к микросервису
AUTH_SERVICE_URL = "http://auth_service:8000/api/v1/auth/user?token="


async def get_current_user(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(AUTH_SERVICE_URL + token)
        return response.json()