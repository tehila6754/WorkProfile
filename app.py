from typing import List
from flask import Flask, render_template, request, Response
from os import environ
from dbcontext import db_data, db_delete, db_add, health_check
from person import Person
import logging

app = Flask(__name__)

@app.route("/health")
def health():
    health_messages = []
  
    try:
        app.logger.info("Application is running")
        health_messages.append("Application: Healthy")
    except Exception as e:
        app.logger.error(f"Application health check failed: {e}")
        health_messages.append("Application: Not Healthy")
    combined_health_status = "\\\\n".join(health_messages)
    return combined_health_status

app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

host_name = environ.get("HOSTNAME")
if not health_check():
    host_name = "no_host"
db_host = environ.get('DB_HOST')
backend = environ.get('BACKEND') or "http://localhost"

@app.route("/")
def main():
    app.logger.info("Entering main route")
    data: List[Person] = db_data()  # Assuming db_data returns a list of Person
    return render_template("index.html.jinja", host_name=host_name, db_host=db_host, data=data, backend=backend)

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id: int):
    app.logger.info("Request to delete person with id: %s", id)
    return db_delete(id)

@app.route("/add", methods=["PUT"])
def add():
    body = request.json
    if body is not None:
        app.logger.info("Request to add person with body: %s", body)
        person = Person(0, body["firstName"], body["lastName"], body["age"], body["address"], body["workplace"])
        return db_add(person)
    app.logger.error("Request body is empty")

    return Response(status=404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
