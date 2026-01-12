Performance Optimization Demo (Python + MySQL + Redis)

This project demonstrates real-world application performance optimization using DevOps and backend best practices.
It shows a measurable before-and-after comparison using load testing.

Project Objective:

To identify performance bottlenecks in a backend application and improve:

    1. API response time

    2. Throughput (requests per second)

    3. Stability under concurrent load

All improvements are validated using load testing metrics.

Tech Stack:
Application

    * Python (Flask)

    * MySQL 8

    * Redis (caching)

DevOps & Infrastructure

    * Docker & Docker Compose

    * Linux (Ubuntu)

    * Container networking & health checks

Testing & Validation

    * k6 (load testing)

Architecture Overview:

Client
  |
  | HTTP
  v
Flask API (Docker)
  |
  | Cache lookup
  v
Redis (in-memory)
  |
  | Fallback (miss)
  v
MySQL Database

Test Scenario:-

    Endpoint tested: GET /products

    Virtual users (VUs): 50

    Duration: 2 minutes

    Tool: k6

    Same infrastructure for before & after tests

Before Optimization (Baseline)
Characteristics:

    Every request hits MySQL

    No caching

    Artificial delay simulating real-world slowness

Load Test Results:

    Average response time: ~363 ms

    p95 latency: ~434 ms

    Throughput: ~36 requests/sec

    Errors: 0%

Issues Identified:

    Database was the primary bottleneck

    Repeated identical queries

    Poor scalability under load

Optimization Applied:
Improvements Made

    Introduced Redis caching

    Reduced database calls drastically

    Ensured proper container startup ordering with health checks

    Kept infrastructure unchanged (cost-efficient)

Key Principle:-

    Cache frequently accessed, read-heavy data to reduce database load.

After Optimization (Improved)
Load Test Results

    Average response time: ~8.9 ms

    p95 latency: ~8.3 ms

    Throughput: ~49 requests/sec

    Errors: 0%

| Metric            | Before    | After     | Improvement           |
| ----------------- | --------- | --------- | --------------------- |
| Avg Response Time | ~363 ms   | ~8.9 ms   | **~40× faster**       |
| p95 Latency       | ~434 ms   | ~8.3 ms   | **Massive reduction** |
| Throughput        | ~36 req/s | ~49 req/s | **~36% increase**     |
| Error Rate        | 0%        | 0%        | No regression         |

Start Services:- 
    docker-compose up -d --build

Test API:-
    curl http://localhost:5000/products

Run Load Test:-
    k6 run load.js