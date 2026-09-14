# Exercise 02 — Streamlit Dashboard (Frontend + API + PostgreSQL)

> **Distributed Systems & Parallel Programming — UNLu 2026**
>
> This exercise is part of the continuous assessment for the course. Throughout the semester you will solve hands-on exercises that are graded automatically. Each exercise builds on the previous one and reinforces concepts you will need for the major assignments: REST APIs, Docker, Compose, Kubernetes, messaging, etc.
>
> The goal is not just to "pass the tests" but to understand what you are building. Tests validate the output — comprehension is on you.

## Course topics covered

| Unit | Topic | How it applies here |
|------|-------|-------------------|
| **U4.3** | Docker Compose: multi-container applications | You orchestrate 3 services: frontend, API, and database |
| **U1.6** | Client-Server communication, HTTP, JSON | The frontend consumes the REST API as a client |

### What you will practice

- Building a **web frontend** with Streamlit that consumes a REST API
- Running **3-service Docker Compose** stacks (frontend + backend + database)
- Understanding **service-to-service communication** inside a Docker network

---

## Automated grading

Every time you push to your fork, we will run a set of hidden tests. Within 10 minutes you will receive a ✅/❌ comment on your latest commit.

Hidden tests cover:
- docker-compose.yml has 3 services (frontend, api, db)
- Frontend responds on port 8501
- Frontend displays node list from the API
- Registering a node via API appears in the frontend
- Frontend Dockerfile follows best practices
- Backend API still works (all 6 endpoints)

You have a maximum of **5 submissions**. It is a nice challenge — let us build it together.

**Deadline: Sunday, October 4, 2026 at 23:59 (UTC-3)** (2 late days allowed with penalty)

---

## Context

In Exercise 01 you built a Node Registry API. Now you add a user interface so humans can interact with the system visually — a common pattern in microservice architectures.

## Objective

Add a **Streamlit frontend** to the Node Registry. The result is a 3-service Docker Compose stack.

## How to submit

1. **Fork** this repo
2. Implement `frontend/app.py` (Streamlit dashboard)
3. Implement `frontend/Dockerfile`
4. Implement `docker-compose.yml` (3 services)
5. Run locally: `docker compose up --build`
6. Verify: open `http://localhost:8501` in your browser
7. Push to your fork

---

## What the frontend must show

| Feature | Description |
|---------|-------------|
| **Node list** | Table showing all registered nodes (name, host, port, status) |
| **Register form** | Input fields for name, host, port + submit button |
| **Delete button** | Button to soft-delete a node by name |
| **Health indicator** | Shows API health status and active node count |

## What to deliver

| File | Description |
|------|-------------|
| `frontend/app.py` | Streamlit application |
| `frontend/Dockerfile` | Production-ready (non-root, slim, EXPOSE 8501) |
| `docker-compose.yml` | 3 services: db, api, frontend |
| Everything from Exercise 01 | Backend is provided as starter code |

## Docker requirements

### frontend service
- Build from `frontend/Dockerfile`
- Expose port **8501**
- `depends_on` the api service
- Pass `API_URL=http://api:8080` as environment variable

## Running locally

```bash
docker compose up --build -d
# Frontend: http://localhost:8501
# API: http://localhost:8080/health
docker compose down -v
```
