# XENYOU PROJECT

## 🔑 Operations flow

- Student types a query (structured or natural language) into the Frontend UI.

- Query goes to FastAPI Gateway → routes to Search & Recommendation service.

- If natural language, NLP Parser (OpenAI/HuggingFace) converts it → filters.

- Filters + embeddings go into pgvector/FAISS for semantic matching.

- Results re-ranked with CF recommender (based on student history).

- Ranked hostel list returned → frontend shows cards + chat-style response.

- All interactions (clicks, saves, bookings) logged in Analytics Service.

- Periodic jobs (Celery) retrain models → updated recommender served via API.

## SCALFFOLDING

Python project scaffold for XenYou (FastAPI + PostgreSQL + pgvector-ready + embeddings demo).

This will give you:

✅ FastAPI backend (/search endpoint)

✅ SQLModel ORM + Postgres connection

✅ Embedding generator (sentence-transformers)

✅ FAISS in-memory index (easy to swap later for pgvector/Pinecone)

✅ Simple project structure ready for expansion

## Start API

uvicorn app.main:app --reload

## 🔧 Setup pgvector

embeddings are stored and queried directly inside PostgreSQL with pgvector instead of FAISS.This makes the system persistent and production-ready.

### 🔑 Why pgvector > FAISS here

✅ Persistent in DB (no need to rebuild index on restart)

✅ Works with SQL joins + filters (budget, distance) in one query

✅ Easy to scale (just add embeddings column & index)

## Interaction Logging Service

 → Track what students do (click, save, apply).

## Recommender Service (LightFM stub)

 → Train a hybrid (content + collaborative filtering) model. Run as background training job for now.

## Background Task Setup

FastAPI BackgroundTasks (for lightweight jobs). To be later scaled up with Celery + Redis if needed.

### Celery + Redis

For More Control (Celery + Redis)
For production scale:

- Use Celery Beat (scheduler) + Redis or RabbitMQ.

- This gives you retry, monitoring, distributed workers.

    Example: run training every midnight UTC automatically.

#### 🚀 Workflow Now

- Add students + hostels.

- Students interact (click/save/apply).

- Recommender auto-trains daily in the background.

- Students get fresh, personalized hostel recommendations.



## Database Design
🧠 Overview of Key Entities

- User (Base model) — Shared fields for all users.

- Student — Inherits from User.

- Landlord — Inherits from User.

- Property — Apartment/listing owned by a landlord.

- Verification — Stores landlord verification data (e.g. ID, CAC doc).

- Match — Connects students with properties.

- Admin — Internal management users.



| Role     | Auth Source | Profile Table     | Verification           | Key Privileges                        |
| -------- | ----------- | ----------------- | ---------------------- | ------------------------------------- |
| Student  | users       | student_profiles  | student_verifications  | Search & match apartments             |
| Landlord | users       | landlord_profiles | landlord_verifications | Create and manage listings            |
| Admin    | users       | admin_profiles    | (optional)             | Approve verifications, oversee system |


User ─┬─< Student
       ├─< Landlord ──< Property ──< Match >─ Student
       └─< Admin

Landlord ──< Verification

