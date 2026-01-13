**Performance Optimization & Async Processing Demo**

Flask · Redis · Celery · MySQL · Docker · k6

**Overview**

This project demonstrates how to design, optimize, and validate a backend system by moving from a synchronous architecture to an asynchronous, production-grade architecture using Celery and Redis.

The goal was to:

    Improve API responsiveness under load

    Isolate CPU and database-intensive work

    Maintain SLA guarantees under concurrent traffic

    Validate improvements using k6 load testing

**Architecture**
Before (Synchronous)

    Flask handled CPU-heavy + DB-heavy logic directly in request threads

    Fast at low load but risked thread blocking and poor scalability

After (Asynchronous)

    Flask API enqueues heavy tasks to Celery

    Redis acts as message broker and result backend

    Celery workers execute heavy jobs independently

    Redis cache used for read-heavy endpoints

Key benefit: Request threads remain free, improving stability and scalability.

**Tech Stack**

 Component               | Purpose                     
 ----------------------- | --------------------------- 
 Flask                   | REST API                    
 MySQL                   | Persistent storage          
 Redis                   | Cache + Celery broker       
 Celery                  | Async background processing 
 Docker & Docker Compose | Containerized services      
 k6                      | Load & SLA testing          

 **API Endpoints**

  Endpoint          | Description                   
 ------------------ | ----------------------------- 
 `/health`          | Service health check          
 `/products`        | Read-heavy API (Redis-cached) 
 `/heavy-process`   | Enqueues CPU + DB heavy job   
 `/job-status/<id>` | Tracks background task status 

**Async Flow (/heavy-process)**

    Client calls /heavy-process

    Flask immediately enqueues job to Redis

    Celery worker picks up job

    Worker executes CPU-heavy + DB logic

    Result stored in Redis

    Client polls /job-status/<id> for completion

This decouples request handling from heavy computation.

**Performance Testing (k6)**
Test Configuration

    50 Virtual Users

    2 minutes duration

    SLA thresholds:

        Heavy endpoint p95 < 100 ms

        Products endpoint p95 < 50 ms

        Error rate < 1%

**Key Learnings**

Asynchronous processing slightly increases enqueue latency but massively improves scalability and reliability

Tail latency matters more than average latency in production systems

depends_on ≠ service readiness → retries are essential

Celery task registration and isolation are critical

Performance optimization is about system behavior under load, not just raw speed

**Validation Outcome**

All SLAs met under concurrent load

Zero request failures

Stable throughput (~49 RPS)

Improved tail latency and fault isolation