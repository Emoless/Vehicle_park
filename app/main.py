import time
from fastapi import FastAPI
from database import get_connection
from routers import drivers, tasks, vehicles, administrators
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",  # Разрешить доступ с локального хоста
    "http://localhost:3000",  # Разрешить доступ с фронтенда на порту 3000 (если используется)
    "http://127.0.0.1",  # Разрешить доступ с 127.0.0.1
    "http://127.0.0.1:3000",  # Разрешить доступ с фронтенда на порту 3000 (если используется)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Используем список разрешённых доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (POST, GET, OPTIONS, и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Подключение к базе данных
while True:
    try:
        conn = get_connection()
        print("Connection to DB is OK.")
        break
    except Exception as e:
        print("Connection to DB is FAILED.")
        print("Error: ", e)
        time.sleep(3)

# Подключение роутеров
app.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(administrators.router, prefix="/administrators", tags=["Administrators"])

@app.get("/")
async def root():
    return {"message": "Hi!"}
