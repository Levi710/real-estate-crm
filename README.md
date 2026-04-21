# 🏠 Real Estate CRM System
> End-to-end Data Engineering Capstone Project

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://real-estate-crm-ayushkishor.streamlit.app/)

A complete Real Estate CRM built with PostgreSQL, Python ETL pipeline, Streamlit analytics dashboard, FastAPI backend, Apache Airflow, Kafka, PySpark, and streaming simulation.

🔗 **Live Demo** → https://real-estate-crm-ayushkishor.streamlit.app/

---

## 📌 Project Overview

This project simulates a real-world real estate business data system — tracking agents, clients, properties, listings, leads, transactions, and interactions. It covers the full data engineering lifecycle from schema design to analytics, streaming, orchestration, and visualization.

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
│            (Docker locally / Neon on cloud)             │
│                                                         │
│  agents │ clients │ properties │ listings │ leads       │
│              transactions │ interactions                │
└──────────────────┬──────────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌───────────────┐
│ FastAPI  │ │Streamlit │ │    Airflow    │
│ Backend  │ │Dashboard │ │  Scheduler   │
└──────────┘ └──────────┘ └───────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Kafka Pipeline                         │
│  Producer → topic: properties → Consumer → PostgreSQL  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  PySpark Jobs                           │
│  Load CSV → Transform → SQL → Partition → Cache        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 15 (Docker / Neon) |
| Data Generation | Python, Faker |
| ETL Pipeline | Python, Pandas, psycopg2 |
| Analytics | SQL (Window functions, JOINs, Aggregations) |
| Dashboard | Streamlit, Plotly |
| Backend API | FastAPI, Uvicorn |
| Orchestration | Apache Airflow 2.8 |
| Streaming | Kafka, Zookeeper, Stream Simulator |
| Big Data | PySpark 3.5 |
| Data Quality | Custom validation checks |
| Containerization | Docker, Docker Compose |
| Cloud DB | Neon PostgreSQL |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
real-estate-crm/
│
├── docker-compose.yml       # All services config
├── schema.sql               # Database schema (7 tables)
├── setup.sh                 # Automated setup script
├── requirements.txt         # Python dependencies
│
├── etl/
│   ├── seed.py              # Fake data generation
│   ├── generate_csv.py      # CSV generator with dirty data
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
├── dags/
│   └── etl_dag.py           # Airflow DAG (daily ETL schedule)
│
├── kafka/
│   ├── producer.py          # Kafka property publisher
│   └── consumer.py          # Kafka consumer → PostgreSQL
│
├── streaming/
│   └── stream_simulator.py  # Real-time property feed simulation
│
├── spark/
│   └── spark_jobs.ipynb     # PySpark jobs (Tasks 14-17)
│
├── quality/
│   └── data_quality.py      # Data validation report
│
├── data/
│   ├── new_clients.csv
│   └── new_properties.csv
│
└── docs/
    └── Real_Estate_CRM_Ayush_Kishor_23053515.pdf
```

---

## ✅ Data Engineering Tasks Covered

| Task | Description | Status |
|---|---|---|
| Task 1 | Linux + Shell script automation | ✅ |
| Task 3 | Python CSV processing + cleaning | ✅ |
| Task 6 | SQL basics (SELECT, WHERE, GROUP BY) | ✅ |
| Task 7 | Advanced SQL (JOINs, subqueries, window functions) | ✅ |
| Task 10 | ETL pipeline | ✅ |
| Task 11 | Batch ingestion from CSV to database | ✅ |
| Task 14 | Spark basics — process dataset | ✅ |
| Task 15 | Spark DataFrames — transformations | ✅ |
| Task 16 | Spark SQL — query large dataset | ✅ |
| Task 17 | PySpark advanced — partitioning + caching | ✅ |
| Task 18 | Streaming concepts simulation | ✅ |
| Task 19 | Kafka basics — producer-consumer | ✅ |
| Task 20 | Kafka advanced — offset management | ✅ |
| Task 22 | Airflow DAG for ETL pipeline | ✅ |
| Task 23 | Airflow scheduling + monitoring | ✅ |
| Task 29 | Data quality validation checks | ✅ |
| Task 30 | Final end-to-end pipeline | ✅ |

---

## 🚀 How to Run Locally

### Prerequisites
- Docker Desktop
- Python 3.10+
- Git Bash (for shell script)

### 1. Clone and setup
```bash
git clone https://github.com/Levi710/real-estate-crm
cd real-estate-crm
bash setup.sh
```

### 2. Create `.env` file
```
DATABASE_URL=postgresql://admin:password@127.0.0.1:5433/realestate_crm
```

### 3. Start all services
```bash
docker compose up -d
```

### 4. Create schema + seed data
```bash
docker cp schema.sql realestate_crm_db:/schema.sql
docker exec -it realestate_crm_db psql -U admin -d realestate_crm -f /schema.sql
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

### 8. Run Kafka pipeline
```bash
# Terminal 1
python kafka/consumer.py
# Terminal 2
python kafka/producer.py
```

### 9. Run streaming simulation
```bash
python streaming/stream_simulator.py
```

### 10. Run data quality checks
```bash
python quality/data_quality.py
```

### 11. Access Airflow
```
http://localhost:8088
```

### 12. Access Jupyter/PySpark
```
http://localhost:8890
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
LinkedIn: [ayush-kishor](https://linkedin.com/in/ayush-kishor-b3b5312a6)
Portfolio: [kishorayush.online](https://kishorayush.online)