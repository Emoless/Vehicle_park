from fastapi import APIRouter, Response
from database import get_connection
from models import Driver
from utils import hash_password
from psycopg2 import errors
from fastapi import HTTPException, status

router = APIRouter()
conn = get_connection()
cursor = conn.cursor()

# Drivers -> GET

@router.get("/all")
async def get_all_drivers():
    cursor.execute("""SELECT * FROM Driver""")
    query = cursor.fetchall()
    return {"All Drivers": query}

@router.get("/available")
async def get_available_drivers():
    cursor.execute(""" SELECT * FROM Driver 
                   Where status = 'available'""")
    query = cursor.fetchall()
    return {"Available Drivers": query}

@router.get("/unavailable")
async def get_unavailable_drivers():
    cursor.execute(""" SELECT * FROM Driver 
                   Where status = 'unavailable'""")
    query = cursor.fetchall()
    return {"Available Drivers": query}

@router.get("/{id}")
async def get_driver_by_id(id: int):
    cursor.execute("""SELECT * FROM Driver WHERE id = %s""", (id,))
    query = cursor.fetchall()
    return {f"Driver with id {id}": query}

# Drivers -> POST

@router.post("/add")
async def add_driver(driver: Driver):
    try:
        hashed_password = hash_password(driver.password)
        cursor.execute("""
            INSERT INTO Driver (name, experience, phone, email, password) 
            VALUES (%s, %s, %s, %s, %s) RETURNING *""", 
            (driver.name, driver.experience, driver.phone, driver.email, hashed_password)
        )
        new_driver = cursor.fetchone()
        conn.commit()
        return {"New driver added": new_driver}

    except errors.UniqueViolation as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists. Please provide a different email."
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Drivers -> DELETE

@router.delete("/{id}")
async def delete_driver(id: int, response: Response):
    cursor.execute("""DELETE FROM Driver WHERE id = %s RETURNING *""", (id,))
    deleted_driver = cursor.fetchone()
    conn.commit()
    if deleted_driver:
        return {"Driver deleted": deleted_driver}
    else:
        response.status_code = 404
        return {"error": "Driver not found"}
