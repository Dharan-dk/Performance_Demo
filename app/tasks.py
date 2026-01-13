import time
import math
import mysql.connector
from celery_app import celery

def get_db(retries=5, delay=3):
    for attempt in range(retries):
        try:
            return mysql.connector.connect(
                host="mysql",
                user="demo",
                password="demo",
                database="demo",
                connection_timeout=5
            )
        except mysql.connector.Error:
            if attempt == retries - 1:
                raise
            time.sleep(delay)

@celery.task(
    bind=True,
    name="tasks.heavy_job",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True
)
def heavy_job(self):
    start = time.time()

    total = 0
    for i in range(1, 20000):
        total += math.sqrt(i) * math.log(i + 1)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    time.sleep(0.5)

    duration = round(time.time() - start, 3)

    return {
        "status": "completed",
        "products_count": count,
        "processing_time_seconds": duration
    }
