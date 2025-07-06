import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "flaskapp"),
        password=os.getenv("DB_PASS", "flaskapp"),
        database=os.getenv("DB_NAME", "exampleDb")
    )

def db_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()
    conn.close()
    return rows

def db_add(person):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO people (firstName, lastName, age, address, workplace) VALUES (%s, %s, %s, %s, %s)"
    values = (person.firstName, person.lastName, person.age, person.address, person.workplace)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return "Inserted"

def db_delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM people WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return "Deleted"

def health_check():
    try:
        conn = get_connection()
        conn.ping()
        return True
    except:
        return False

