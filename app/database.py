import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Vehicle_park",
        user="postgres",
        password="1111",
        cursor_factory=RealDictCursor
    )
