from flask import Flask, jsonify

app = Flask(__name__)

# נתונים זמניים בזיכרון (רשימת עובדים לדוגמה)
employees = [
    {"id": 1, "firstName": "Tzivi", "lastName": "Blui", "age": 30, "address": "Tel Aviv", "workplace": "Company A"},
    {"id": 2, "firstName": "John", "lastName": "Doe", "age": 40, "address": "Jerusalem", "workplace": "Company B"}
]

@app.route("/")
def main():
    return jsonify(employees)

@app.route("/health")
def health():
    return jsonify({"application": "Healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
