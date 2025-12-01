from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "mydatabase"),
        user=os.getenv("POSTGRES_USER", "myuser"),
        password=os.getenv("POSTGRES_PASSWORD", "mypassword"),
    )
    return conn


@app.post("/expense")
def save_expense():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "error": "No JSON received"}), 400

    try:
        ts = datetime.fromisoformat(data["date"])
        amount = float(data["amount"])
        bank = data.get("bank")
        payment_method = data.get("payment_method")
        category = data.get("category")
        description = data.get("description")
    except Exception as e:
        return jsonify({"ok": False, "error": f"Bad payload: {e}"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO expense (ts, payment_method, bank, amount, category, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (ts, payment_method, bank, amount, category, description),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"ok": False, "error": f"DB error: {e}"}), 500

    return jsonify({"ok": True})



@app.get("/")
def health():
    return {"status": "running"}


if __name__ == "__main__":
    # Para probar local, si quieres
    app.run(host="0.0.0.0", port=8080)
