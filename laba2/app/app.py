# еле написал, брал конфиги у чувака с гитхаба # немножнко пидор
import os
from flask import Flask, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv('PG_HOST'),
        port=int(os.getenv('PG_PORT')),
        database=os.getenv('PG_NAME'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        cursor_factory=RealDictCursor
    )

@app.route("/users", methods=["GET"])
def list_users():
    limit = request.args.get('limit', 10, type=int)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, surname, age, town FROM users ORDER BY id LIMIT %s", (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, surname, age, town FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        abort(404)
    return jsonify(dict(row))

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, surname, age, town) VALUES (%s, %s, %s, %s) RETURNING id",
        (data['name'], data['surname'], data['age'], data['town'])
    )
    new_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, **data}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name=%s, surname=%s, age=%s, town=%s WHERE id=%s RETURNING id",
        (data['name'], data['surname'], data['age'], data['town'], user_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        abort(404)
    return jsonify({"id": user_id, **data})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted == 0:
        abort(404)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
