import os
import time
import traceback
from flask import Flask, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Глобальная переменная для времени начала запроса
start_time = None

# Метрики Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency in seconds',
    ['endpoint']
)

DB_ERRORS = Counter(
    'db_errors_total', 'Total DB errors'
)

@app.before_request
def before_request():
    global start_time
    start_time = time.time()

@app.after_request
def track_after_request(response):
    global start_time
    if start_time:
        endpoint = request.path
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            request.method, 
            endpoint, 
            str(response.status_code)
        ).inc()
        REQUEST_LATENCY.labels(endpoint).observe(duration)
    return response

@app.errorhandler(Exception)
def handle_error(error):
    global start_time
    if start_time:
        endpoint = request.path
        duration = time.time() - start_time
        status = "500"
        if hasattr(error, 'code'):
            status = str(error.code)
        REQUEST_COUNT.labels(request.method, endpoint, status).inc()
        REQUEST_LATENCY.labels(endpoint).observe(duration)
    if hasattr(error, 'code'):
        return jsonify({"error": str(error)}), error.code
    return jsonify({"error": "Internal Server Error"}), 500

def get_db():
    try:
        return psycopg2.connect(
            host=os.getenv('PG_HOST'),
            port=int(os.getenv('PG_PORT')),
            database=os.getenv('PG_NAME'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        DB_ERRORS.inc()
        raise

# Metrics endpoint для Prometheus
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# тестовые роуты
@app.route('/test/200')
def test_200():
    return jsonify({"status": "OK"}), 200

@app.route('/test/400')
def test_400():
    abort(400)

@app.route('/test/404')
def test_404():
    abort(404)

@app.route('/test/409')
def test_409():
    return jsonify({"error": "Conflict"}), 409

@app.route('/test/500')
def test_500():
    1 / 0  
    return "OK"

@app.route('/test/slow')
def test_slow():
    time.sleep(2)
    return jsonify({"status": "slow OK"}), 200

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
    if not data or 'name' not in data:
        abort(400)
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
    if not data or 'name' not in data:
        abort(400)
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
    app.run(debug=True, host='0.0.0.0', port=8000)
