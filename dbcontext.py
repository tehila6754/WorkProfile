from unittest import result
import mysql.connector
from os import environ
from person import Person
from flask import Response
from typing import List

db_user = environ.get('DB_USER')
db_pass = environ.get('DB_PASS')
db_host = environ.get('DB_HOST')
db_name = environ.get('DB_NAME')

config = {
    "host": db_host,
    "user": db_user,
    "password": db_pass,
    "database": db_name,
    "port": 3306
}

def db_data() -> List[Person]:
    if not db_host:
        return demo_data()  # פונקציה שאתה מגדיר במקרה שאין חיבור למסד נתונים.

    if not (db_user and db_pass):
        raise Exception("DB_USER and DB_PASS are not set")

    cnx = mysql.connector.connect(**config)
    result = []
    if cnx.is_connected():
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT * FROM people")
            for item in cursor:
                result.append(Person(item[0], item[1], item[2], item[3], item[4], item[5]))
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
    return result

def db_delete(id: int) -> Response:
    if not db_host:
        return Response(status=200)
    
    cnx = mysql.connector.connect(**config)
    status = 200
    if cnx.is_connected():
        cursor = cnx.cursor()
        try:
            cursor.execute(f"DELETE FROM people WHERE id = {id}")
            cnx.commit()
        except Exception as e:
            status = 404
            print(f"Error deleting: {e}")
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
    return Response(status=status)

def db_add(person: Person) -> Response:
    if not db_host:
        return Response(status=200)
    
    cnx = mysql.connector.connect(**config)
    status = 200
    personId = 0
    if cnx.is_connected():
        cursor = cnx.cursor()
        try:
            cursor.execute(f"INSERT INTO people (firstName, lastName, age, address, workplace) VALUES ('{person.first_name}', '{person.last_name}', {person.age}, '{person.address}', '{person.workplace}')")
            cnx.commit()
            personId = cursor.lastrowid
        except Exception as e:
            status = 404
            print(f"Error adding: {e}")
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
    return Response(status=status, response=str(personId))

def health_check() -> bool:
    if not db_host:
        return True
    
    cnx = mysql.connector.connect(**config)
    response = False
    if cnx.is_connected():
        cursor = cnx.cursor()
        try:
            cursor.execute("SELECT 1")
            cursor.fetchall()
            response = True
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
    return response

