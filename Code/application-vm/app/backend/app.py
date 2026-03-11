from flask import Flask, request, jsonify, make_response
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# Global CORS handler
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# Login route
@app.route("/login", methods=["POST", "OPTIONS"])
def login():

    # Handle browser preflight request
    if request.method == "OPTIONS":
        return make_response("", 200)

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing credentials"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM users WHERE username = %s AND password = %s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
