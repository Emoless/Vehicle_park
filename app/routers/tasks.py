from fastapi import APIRouter, Response
from database import get_connection
from models import Task
from psycopg2 import errors
from fastapi import HTTPException, status

router = APIRouter()
conn = get_connection()
cursor = conn.cursor()

# Tasks -> GET

@router.get("/all")
async def get_all_tasks():
    cursor.execute("""SELECT * FROM Task""")
    query = cursor.fetchall()
    return {"All Tasks": query}

@router.get("/current")
async def get_current_tasks():
    cursor.execute(""" SELECT * FROM Task 
                   WHERE status = 'assigned'""")
    query = cursor.fetchall()
    return {"Current tasks": query}

@router.get("/finished")
async def get_finished_tasks():
    cursor.execute(""" SELECT * FROM Task 
                   WHERE status = 'completed'""")
    query = cursor.fetchall()
    return {"Finished tasks": query}

@router.get("/{id}")
async def get_task_by_id(id: int):
    cursor.execute("""SELECT * FROM Task WHERE id = %s""", (id,))
    query = cursor.fetchone()
    return {"Task": query}

# Tasks -> POST

@router.post("/add")
async def add_task(task: Task):
    try:
        cursor.execute(
            """INSERT INTO Task (route, driver_id, car_id) VALUES (%s, %s, %s) RETURNING *""",
            (task.route, task.driver_id, task.car_id)
        )
        new_task = cursor.fetchone()
        conn.commit()
        return {"New task added": new_task}

    except errors.ForeignKeyViolation as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid driver_id or car_id. Please ensure both the driver and vehicle exist."
        )
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# Tasks -> UPDATE

@router.put("/update/{id}")
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
    
# Tasks -> DELETE

@router.delete("/{id}")
async def delete_task(id: int, response: Response):
    cursor.execute("""DELETE FROM Task WHERE id = %s RETURNING *""", (id,))
    deleted_task = cursor.fetchone()
    conn.commit()
    if deleted_task:
        return {"Task deleted": deleted_task}
    else:
        response.status_code = 404
        return {"error": "Task not found"}
