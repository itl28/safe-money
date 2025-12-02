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


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/expense")
def save_expense():
    """
    JSON esperado (tal como lo guarda tu gastos.json):

    {
      "date": "2025-11-28T13:53:00-06:00",
      "payment_method": "APPLE PAY/CARD",
      "bank": "BBVA",
      "amount": 65,
      "type": "Comida",
      "desc": "Café "
    }
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"ok": False, "error": "No JSON received"}), 400

    try:
        # 'date' viene en formato ISO con zona horaria (-06:00)
        ts = datetime.fromisoformat(data["date"])
        amount = float(data["amount"])

        payment_method = data.get("payment_method")
        bank = data.get("bank")
        category = data.get("type")   # va a la columna 'category'
        description = data.get("desc")  # va a la columna 'description'
    except KeyError as e:
        return jsonify({"ok": False, "error": f"Missing field: {e}"}), 400
    except ValueError as e:
        return jsonify({"ok": False, "error": f"Bad value: {e}"}), 400
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
