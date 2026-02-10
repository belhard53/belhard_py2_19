from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

# Первый эндпоинт - главная страница
async def homepage(request):
    return JSONResponse({"message": "Hello from Starlette!", "status": "ok"})

# Второй эндпоинт - информация о пользователе
async def user_info(request):
    return JSONResponse({
        "user": "example_user",
        "id": 123,
        "active": True
    })

# Создаем приложение с двумя маршрутами
app = Starlette(routes=[
    Route("/", homepage),
    Route("/user", user_info),
])

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)