from flask import Flask, jsonify
import mysql.connector
import redis
import time
import json
import math
import uuid
import threading

app = Flask(__name__)

# Redis connection
cache = redis.Redis(host="redis", port=6379, decode_responses=True)

# MySQL connection
def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="demo",
        password="demo",
        database="demo"
    )

# --------------------------------------------------
# 1️⃣ FAST API – Read-heavy (CACHEABLE)
# --------------------------------------------------
@app.route("/products")
def products():
    cached_data = cache.get("products")

    if cached_data:
        return jsonify(json.loads(cached_data))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    # Cache for 60 seconds
    cache.setex("products", 60, json.dumps(data))

    return jsonify(data)

# --------------------------------------------------
# 2️⃣ SLOW API – CPU + DB heavy (INTENTIONAL)
# --------------------------------------------------
# @app.route("/heavy-process")
# def heavy_process():
#     start = time.time()

#     # Simulate CPU-heavy work
#     total = 0
#     for i in range(1, 20000):
#         total += math.sqrt(i) * math.log(i + 1)

#     # Simulate DB-heavy operation
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT COUNT(*) FROM products")
#     count = cursor.fetchone()[0]

#     # Simulate additional latency
#     time.sleep(0.5)

#     duration = round(time.time() - start, 3)

#     return jsonify({
#         "status": "completed",
#         "products_count": count,
#         "processing_time_seconds": duration
#     })

@app.route("/heavy-process")
def heavy_process():
    job_id = str(uuid.uuid4())

    cache.setex(f"job:{job_id}", 300, json.dumps({
        "status": "processing"
    }))

    thread = threading.Thread(target=run_heavy_job, args=(job_id,))
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    }), 202

def run_heavy_job(job_id):
    start = time.time()

    # CPU-heavy simulation
    total = 0
    for i in range(1, 20000):
        total += math.sqrt(i) * math.log(i + 1)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    time.sleep(0.5)

    duration = round(time.time() - start, 3)

    cache.setex(
        f"job:{job_id}",
        300,
        json.dumps({
            "status": "completed",
            "products_count": count,
            "processing_time_seconds": duration
        })
    )

@app.route("/job-status/<job_id>")
def job_status(job_id):
    result = cache.get(f"job:{job_id}")
    if not result:
        return jsonify({"status": "not_found"}), 404
    return jsonify(json.loads(result))

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)