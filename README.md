# 🏠 Real Estate CRM System
> End-to-end Data Engineering Capstone Project

A complete Real Estate CRM built with PostgreSQL, Python ETL pipeline, Streamlit analytics dashboard, and FastAPI backend.

---

## 📌 Project Overview

This project simulates a real-world real estate business data system — tracking agents, clients, properties, listings, leads, transactions, and interactions. It covers the full data engineering lifecycle from schema design to analytics and visualization.

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                         │
│         CSV Files          +       Faker (Seed)         │
└────────────┬───────────────────────────┬────────────────┘
             │                           │
             ▼                           ▼
┌─────────────────────┐     ┌─────────────────────────┐
│   ETL Pipeline      │     │      Seed Script        │
│  etl/etl_pipeline.py│     │     etl/seed.py         │
│                     │     │                         │
│  Extract (CSV)      │     │  Generate fake data     │
│  Transform (pandas) │     │  Insert via psycopg2    │
│  Load (psycopg2)    │     │                         │
└────────┬────────────┘     └────────────┬────────────┘
         │                               │
         └──────────────┬────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                    │
│                  (Docker Container)                     │
│                                                         │
│  agents │ clients │ properties │ listings │ leads       │
│              transactions │ interactions                │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌─────────────────────┐
│  FastAPI      │    │  Streamlit Dashboard│
│  backend/     │    │  dashboard/app.py   │
│  main.py      │    │                     │
│               │    │  KPI Cards          │
│  GET /agents  │    │  Agent Rankings     │
│  GET /props   │    │  Price by City      │
│  GET /trans   │    │  Lead Conversion    │
└───────────────┘    └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 15 (Docker) |
| Data Generation | Python, Faker |
| ETL Pipeline | Python, Pandas, psycopg2 |
| Analytics | SQL (Window functions, JOINs, Aggregations) |
| Dashboard | Streamlit |
| Backend API | FastAPI, Uvicorn |
| Containerization | Docker, Docker Compose |

---

## 📁 Project Structure

```
real-estate-crm/
│
├── docker-compose.yml       # PostgreSQL container config
├── schema.sql               # Database schema (7 tables)
│
├── etl/
│   ├── seed.py              # Fake data generation & insertion
│   ├── generate_csv.py      # CSV data generator with dirty data
│   └── etl_pipeline.py      # ETL: Extract → Transform → Load
│
├── analytics/
│   └── queries.sql          # 5 analytics SQL queries
│
├── dashboard/
│   └── app.py               # Streamlit dashboard
│
├── backend/
│   └── main.py              # FastAPI REST API
│
└── data/
    ├── new_clients.csv
    └── new_properties.csv
```

---

## 🗄️ Database Schema

7 tables with foreign key relationships:

```
agents ──────────────────────────────┐
clients ─────────────────────────┐   │
properties ──────────────────┐   │   │
                             │   │   │
                        listings ────┤
                             │   │   │
                          leads ─────┤
                             │       │
                      transactions ──┘
                      interactions
```

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop
- Python 3.10+
- pip

### 1. Start PostgreSQL
```bash
docker compose up -d
```

### 2. Install dependencies
```bash
pip install psycopg2-binary pandas faker streamlit fastapi uvicorn
```

### 3. Create schema
```bash
docker cp schema.sql realestate_crm_db:/schema.sql
docker exec -it realestate_crm_db psql -U admin -d realestate_crm -f /schema.sql
```

### 4. Seed the database
```bash
python etl/seed.py
```

### 5. Run ETL pipeline
```bash
python etl/etl_pipeline.py
```

### 6. Launch dashboard
```bash
streamlit run dashboard/app.py
```

### 7. Launch API
```bash
uvicorn backend.main:app --reload
```

---

## 📊 Analytics Queries

| # | Query | Description |
|---|---|---|
| 1 | Top agents by listings | Ranks agents by listing count |
| 2 | Revenue per agent | Total transaction value per agent |
| 3 | Avg price by city | Property market value by location |
| 4 | Payment mode distribution | Most used payment methods |
| 5 | Lead conversion rate | Leads vs closed deals per property |

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/agents` | List all agents |
| GET | `/properties` | List all properties |
| GET | `/transactions` | List all transactions |
| GET | `/docs` | Swagger UI |

---

## 👤 Author

**Ayush Kishor**  
B.Tech CSE, KIIT Deemed University (2023–2027)  
GitHub: [Levi710](https://github.com/Levi710)