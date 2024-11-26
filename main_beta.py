import time
from fastapi import FastAPI, Response
from Vehicle_park.app.models import Administrator, Driver, Vehicle, Task
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
from Vehicle_park.app.utils import hash_password

app = FastAPI()


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='Vehicle_park', user='postgres', password='1111', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to DB is OK.")
        break
    except Exception as e:
        print("Connection to DB is FAILED.")
        print("Error: ", e)
        time.sleep(3)

#BASIC
@app.get("/")
async def root():
    return {"message": "Hi!"}

#Drivers

#Drivers -> GET

@app.get("/drivers/{id}")
async def get_driver_by_id(id):
    cursor.execute(f""" SELECT * FROM Driver
                   Where id = {id} """)
    query = cursor.fetchall()
    return {f"Driver with id {id}": query}

@app.get("/drivers/all")
async def get_all_drivers():
    cursor.execute(""" SELECT * FROM Driver """)
    query = cursor.fetchall()
    return {"All Drivers": query}

@app.get("/drivers/available")
async def get_available_drivers():
    cursor.execute(""" SELECT * FROM Driver 
                   Where status = 'inactive'""")
    query = cursor.fetchall()
    return {"Available Drivers": query}

@app.get("/drivers/unavailable")
async def get_unavailable_drivers():
    cursor.execute(""" SELECT * FROM Driver 
                   Where3 status = 'active'""")
    query = cursor.fetchall()
    return {"Available Drivers": query}

#Drivers -> POST

@app.post("/add/driver")
async def add_driver(driver: Driver):
    hashed_password = hash_password(driver.password)
    cursor.execute(""" INSERT INTO Driver (name, experience, phone, email, password) VALUES (%s, %s, %s, %s, %s)
    RETURNING * """,
    (driver.name, driver.experience, driver.phone, driver.email, hashed_password))
    new_driver = cursor.fetchone()
    conn.commit()
    return{"New driver added": new_driver}


# DELETE -> Driver

@app.delete("/delete/driver/{id}")
async def delete_driver(id: int, response: Response):
    try:
        cursor.execute(""" DELETE FROM Driver WHERE id = %s RETURNING * """, (id,))
        deleted_driver = cursor.fetchone()
        conn.commit()
        if deleted_driver:
            return {"Driver deleted": deleted_driver}
        else:
            response.status_code = 404
            return {"error": "Driver not found"}
    except Exception as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)}


#Tasks

#Tasks -> GET

@app.get("/tasks/{id}")
async def get_task_by_id(id):
    cursor.execute(f""" SELECT * FROM Task
                   Where id = {id} """)
    query = cursor.fetchall()
    return {f"Task with id {id}": query}

@app.get("/tasks/all")
async def get_all_tasks():
    cursor.execute(""" SELECT * FROM Task """)
    query = cursor.fetchall()
    return {"All tasks": query}

@app.get("/tasks/current")
async def get_current_tasks():
    cursor.execute(""" SELECT * FROM Task 
                   WHERE status = 'assigned'""")
    query = cursor.fetchall()
    return {"Current tasks": query}

@app.get("/tasks/finished")
async def get_finished_tasks():
    cursor.execute(""" SELECT * FROM Task 
                   WHERE status = 'completed'""")
    query = cursor.fetchall()
    return {"Finished tasks": query}


#Tasks -> POST

@app.post("/add/task")
async def add_task(task: Task, response: Response):
    try:
        cursor.execute(
            """INSERT INTO Task (route, driver_id, car_id) VALUES (%s, %s, %s)
            RETURNING *""",
            (task.route, task.driver_id, task.car_id)
        )
        new_task = cursor.fetchone()
        conn.commit()
        return {"New task added": new_task}
    except errors.RaiseException as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)} # Возвращаем сообщение об ошибке
    

# UPDATE -> Task

@app.put("/update/task/{id}")
async def update_task_status(id: int, response: Response):
    try:
        cursor.execute(
            """UPDATE Task
               SET status = 'finished'
               WHERE id = %s AND status = 'pending'
               RETURNING *""",
            (id,)
        )
        updated_task = cursor.fetchone()
        conn.commit()
        if updated_task:
            return {"Task updated": updated_task}
        else:
            response.status_code = 404
            return {"error": "Task not found or not in 'pending' status"}
    except Exception as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)}



# DELETE -> Task

@app.delete("/delete/task/{id}")
async def delete_task(id: int, response: Response):
    try:
        cursor.execute(""" DELETE FROM Task WHERE id = %s RETURNING * """, (id,))
        deleted_task = cursor.fetchone()
        conn.commit()
        if deleted_task:
            return {"Task deleted": deleted_task}
        else:
            response.status_code = 404
            return {"error": "Task not found"}
    except Exception as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)}


#Vehicles

#Vehicles -> GET

@app.get("/vehicles/{id}")
async def get_task_by_id(id):
    cursor.execute(f""" SELECT * FROM Vehicle
                   Where id = {id} """)
    query = cursor.fetchall()
    return {f"Vehicle with id {id}": query}

@app.get("/vehicles/all")
async def get_all_vehicles():
    cursor.execute(""" SELECT * FROM Vehicle """)
    query = cursor.fetchall()
    return {"All vehicles": query}

@app.get("/vehicles/available")
async def get_available_vehicles():
    cursor.execute(""" SELECT * FROM Vehicle 
                   WHERE status = 'available'""")
    query = cursor.fetchall()
    return {"Available vehicles": query}

@app.get("/vehicles/unavailable")
async def get_unavailable_vehicles():
    cursor.execute(""" SELECT * FROM Vehicle 
                   WHERE status = 'in_use'""")
    query = cursor.fetchall()
    return {"Unavailable vehicles": query}


#Vehicles -> POST

@app.post("/add/vehicle")
async def add_vehicle(vehicle: Vehicle):
    cursor.execute(""" INSERT INTO Vehicle (brand, reg_num, mileage) VALUES (%s, %s, %s)
    RETURNING * """,
    (vehicle.brand, vehicle.reg_num, vehicle.mileage))
    new_vehicle = cursor.fetchone()
    conn.commit()
    return{"New vehicle added": new_vehicle}


# DELETE -> Vehicle

@app.delete("/delete/vehicle/{id}")
async def delete_vehicle(id: int, response: Response):
    try:
        cursor.execute(""" DELETE FROM Vehicle WHERE id = %s RETURNING * """, (id,))
        deleted_vehicle = cursor.fetchone()
        conn.commit()
        if deleted_vehicle:
            return {"Vehicle deleted": deleted_vehicle}
        else:
            response.status_code = 404
            return {"error": "Vehicle not found"}
    except Exception as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)}



# Administrator -> GET

@app.get("/administrators/all")
async def get_all_administrators():
    try:
        cursor.execute("""SELECT * FROM Administrator""")
        administrators = cursor.fetchall()
        return {"Administrators": administrators}
    except Exception as e:
        return {"error": f"Failed to fetch administrators: {str(e)}"}


@app.get("/administrators/{id}")
async def get_administrator_by_id(id: int, response: Response):
    try:
        cursor.execute("""SELECT * FROM Administrator WHERE id = %s""", (id,))
        administrator = cursor.fetchone()
        if administrator:
            return {"Administrator": administrator}
        else:
            response.status_code = 404
            return {"error": f"Administrator with id {id} not found"}
    except Exception as e:
        response.status_code = 400
        return {"error": f"Failed to fetch administrator: {str(e)}"}

# Administrator -> POST

@app.post("/add/administrator")
async def add_administrator(adminstrator: Administrator, response: Response):
    try:
        hashed_password = hash_password(adminstrator.password)
        cursor.execute(
            """INSERT INTO Administrator (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)
            RETURNING *""",
            (adminstrator.first_name, adminstrator.last_name, adminstrator.email, hashed_password)
        )
        new_administrator = cursor.fetchone()
        conn.commit()
        return {"New administrator added": new_administrator}
    except errors.RaiseException as e:
        conn.rollback()
        response.status_code = 400
        return {"error": str(e)} # Возвращаем сообщение об ошибке

# Administrator -> DELETE

@app.delete("/delete/administrator/{id}")
async def delete_administrator(id: int, response: Response):
    """
    Delete an administrator by ID.
    """
    try:
        cursor.execute("""DELETE FROM Administrator WHERE id = %s RETURNING *""", (id,))
        deleted_admin = cursor.fetchone()
        conn.commit()
        if deleted_admin:
            return {"Administrator deleted": deleted_admin}
        else:
            response.status_code = 404
            return {"error": f"Administrator with id {id} not found"}
    except Exception as e:
        conn.rollback()
        response.status_code = 400
        return {"error": f"Failed to delete administrator: {str(e)}"}
