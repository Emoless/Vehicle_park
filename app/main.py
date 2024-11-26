import time
from fastapi import FastAPI
from database import get_connection
from routers import drivers, tasks, vehicles, administrators

app = FastAPI()

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
