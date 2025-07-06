
from flask import Flask, render_template, request, Response, jsonify
from os import environ
from dbcontext import db_data, db_delete, db_add, health_check
from person import Person
import logging

app = Flask(__name__)

# הגדרת רמת הלוג וה-handler ללוגים
app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# קריאת משתני סביבה
host_name = environ.get("HOSTNAME")
db_host = environ.get('DB_HOST')
backend = environ.get('BACKEND') or "http://localhost"

@app.route("/")
def main():
    app.logger.info("Entering main route")
    data = db_data()
    return render_template("index.html.jinja", host_name=host_name, db_host=db_host, data=data, backend=backend)

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    app.logger.info(f"Request to delete person with id: {id}")
    return db_delete(id)

@app.route("/add", methods=["PUT"])
def add():
    body = request.json
    if body is not None:
        app.logger.info(f"Request to add person with body: {body}")
        person = Person(0, body["firstName"], body["lastName"], body["age"], body["address"], body["workplace"])
        return db_add(person)
    app.logger.error("Request body is empty")
    return Response(status=404)

@app.route("/health")
def health():
    status_code = 200
    health_response = {
        "application": "Healthy",
        "database": "Unknown"
    }
    try:
        # בדיקת חיבור לבסיס הנתונים דרך הפונקציה health_check
        if health_check():
            health_response["database"] = "Healthy"
        else:
            health_response["database"] = "Unhealthy"
            status_code = 503
    except Exception as e:
        app.logger.error(f"Database health check failed: {e}")
        health_response["database"] = "Unhealthy"
        status_code = 503

    app.logger.info(f"Health check response: {health_response}")
    return jsonify(health_response), status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
