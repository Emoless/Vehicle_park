from fastapi import APIRouter, Response
from database import get_connection
from models import Administrator
from utils import hash_password
from psycopg2 import errors
from fastapi import HTTPException, status

router = APIRouter()
conn = get_connection()
cursor = conn.cursor()

# Administrator -> GET

@router.get("/all")
async def get_all_administrators():
    cursor.execute("""SELECT * FROM Administrator""")
    query = cursor.fetchall()
    return {"All Administrators": query}


@router.get("/{id}")
async def get_administrator_by_id(id: int):
    cursor.execute("""SELECT * FROM Administrator WHERE id = %s""", (id,))
    query = cursor.fetchone()
    return {"Administrator": query}

# Administrator -> POST

@router.post("/add")
async def add_administrator(administrator: Administrator):
    try:
        hashed_password = hash_password(administrator.password)
        cursor.execute(
            """INSERT INTO Administrator (first_name, last_name, email, password) 
               VALUES (%s, %s, %s, %s) RETURNING *""",
            (administrator.first_name, administrator.last_name, administrator.email, hashed_password)
        )
        new_administrator = cursor.fetchone()
        conn.commit()
        return {"New administrator added": new_administrator}

    except errors.UniqueViolation as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists. Please provide a different email."
        )
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Administrator -> DELETE

@router.delete("/{id}")
async def delete_administrator(id: int, response: Response):
    cursor.execute("""DELETE FROM Administrator WHERE id = %s RETURNING *""", (id,))
    deleted_administrator = cursor.fetchone()
    conn.commit()
    if deleted_administrator:
        return {"Administrator deleted": deleted_administrator}
    else:
        response.status_code = 404
        return {"error": "Administrator not found"}
