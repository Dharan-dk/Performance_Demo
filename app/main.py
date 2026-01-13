from flask import Flask, jsonify
from celery_app import celery
from tasks import heavy_job
import redis
import json
from mysql.connector import connect

app = Flask(__name__)

cache = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.route("/products")
def products():
    cached = cache.get("products")
    if cached:
        return jsonify(json.loads(cached))

    db = connect(
        host="mysql",
        user="demo",
        password="demo",
        database="demo"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    cache.setex("products", 60, json.dumps(data))
    return jsonify(data)

@app.route("/heavy-process")
def heavy_process():
    task = heavy_job.delay()
    return jsonify({
        "task_id": task.id,
        "status": "queued"
    }), 202

@app.route("/job-status/<task_id>")
def job_status(task_id):
    result = celery.AsyncResult(task_id)

    if result.state == "PENDING":
        return jsonify({"status": "pending"})
    if result.state == "STARTED":
        return jsonify({"status": "processing"})
    if result.state == "SUCCESS":
        return jsonify(result.result)
    if result.state == "FAILURE":
        return jsonify({"status": "failed"}), 500

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)