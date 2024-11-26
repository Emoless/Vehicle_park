from fastapi import APIRouter, Response
from database import get_connection
from models import Vehicle
from psycopg2 import errors
from fastapi import HTTPException, status

router = APIRouter()
conn = get_connection()
cursor = conn.cursor()

# Vehicles -> GET

@router.get("/all")
async def get_all_vehicles():
    cursor.execute("""SELECT * FROM Vehicle""")
    query = cursor.fetchall()
    return {"All Vehicles": query}

@router.get("/available")
async def get_available_vehicles():
    cursor.execute(""" SELECT * FROM Vehicle 
                   WHERE status = 'available'""")
    query = cursor.fetchall()
    return {"Available vehicles": query}

@router.get("/unavailable")
async def get_unavailable_vehicles():
    cursor.execute(""" SELECT * FROM Vehicle 
                   WHERE status = 'in_use'""")
    query = cursor.fetchall()
    return {"Unavailable vehicles": query}

@router.get("/{id}")
async def get_vehicle_by_id(id: int):
    cursor.execute("""SELECT * FROM Vehicle WHERE id = %s""", (id,))
    query = cursor.fetchone()
    return {"Vehicle": query}

# Vehicles -> POST

@router.post("/add")
async def add_vehicle(vehicle: Vehicle):
    try:
        cursor.execute(
            """INSERT INTO Vehicle (brand, reg_num, mileage) VALUES (%s, %s, %s) RETURNING *""",
            (vehicle.brand, vehicle.reg_num, vehicle.mileage)
        )
        new_vehicle = cursor.fetchone()
        conn.commit()
        return {"New vehicle added": new_vehicle}

    except errors.UniqueViolation as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle registration number already exists. Please provide a different registration number."
        )
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Vehicles -> DELETE

@router.delete("/{id}")
async def delete_vehicle(id: int, response: Response):
    cursor.execute("""DELETE FROM Vehicle WHERE id = %s RETURNING *""", (id,))
    deleted_vehicle = cursor.fetchone()
    conn.commit()
    if deleted_vehicle:
        return {"Vehicle deleted": deleted_vehicle}
    else:
        response.status_code = 404
        return {"error": "Vehicle not found"}
