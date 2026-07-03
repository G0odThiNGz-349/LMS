# Learning Management System (LMS) — Data Platform

An end-to-end data platform built on top of a Learning Management System backend, designed to turn raw student, course, and academic activity data into actionable insights through a cloud data pipeline, a machine learning model, and business dashboards.

## Overview

Educational institutions generate large amounts of student data across multiple systems but struggle to turn that data into insights. This project demonstrates how that data can be captured, transformed, and used to understand and improve student performance — from raw transactional records all the way to predictive analytics and executive dashboards.

## Scope

- **LMS Backend** — REST API and relational database for data generation
- **Azure** — Cloud-based data pipelines and data warehouse
- **Machine Learning** — Model for academic performance prediction
- **Dashboards** — Power BI dashboards for business insights

## Architecture

The platform follows a medallion (Bronze/Silver/Gold) architecture:

1. **Data Sources** — APIs (external systems), the main operational database, and manually uploaded CSV files
2. **Raw Data (Bronze / Landing)** — Raw data is copied as-is from the source into cloud storage
3. **Cleansed Data (Silver)** — Data is cleaned and standardized: null handling, deduplication, enum normalization, joining user/student profiles, and feature engineering
4. **Curated Data (Gold)** — Data is modeled into a curated star schema, plus an ML feature store (GPA trend, attendance %, quiz average, failed courses, activity metrics)
5. **Consumption (Analytics & ML)** — Dashboards & reports, machine learning (model training, risk prediction, performance classification, graduation likelihood), and predictions written back to the main database
6. **Analytics & Consumption Layer** — Power BI reports/dashboards, ML insights (at-risk students, intervention alerts, recommendations), and data sharing via CSV/Excel exports or API endpoints

Supporting the pipeline:
- **Orchestration** — Scheduling, retry & failure handling, monitoring and logs
- **Monitoring & Alerts** — Logging & metrics, email/Slack alerts, pipeline monitoring, data quality alerts, model performance alerts
- **Security & Governance** — IAM & access control, role-based access, data encryption, audit logging, data governance

## Backend

### Database Design

The relational schema covers the full academic domain, including:

- `USERS`, `STUDENTS`, `PROFESSORS`, `DEPARTMENTS`
- `COURSES`, `COURSE_PREREQUISITES`, `COURSE_OFFERINGS`, `ACADEMIC_SEMESTERS`
- `ENROLLMENTS`, `ATTENDANCE`
- `QUIZZES` / `QUIZ_SUBMISSIONS`, `EXAMS` / `EXAM_RESULTS`
- `RESOURCES`, `TICKETS`
- `STUDENT_PERFORMANCE` (stores model predictions)

### APIs

Around **91 total APIs**, organized into four groups:

1. Main LMS APIs
2. RBAC APIs (role-based access control)
3. Analytical APIs
4. ML APIs

Example endpoints include `GET /students/me`, `POST /students/`, `GET /students/search`, and `GET /students/year/{academic_year}`, among others covering users, students, professors, courses, enrollments, attendance, and assessments.

Analytical/ML endpoints support **incremental (cursor-based) pagination** — each query filters records greater than the last-seen ID and returns results ordered ascending, which powers the incremental data ingestion pipeline described below.

## Cloud & Data Pipeline (Microsoft Azure)

### Data Ingestion

```
Incremental load from APIs → Store to cloud (Blob Storage) → Transform → Store to warehouse
```

### Incremental Load of Data

1. Data is pulled from analytical APIs using the last-loaded ID as a cursor
2. The new last IDs are persisted to a JSON file (`max_ids`) so subsequent runs only fetch new records
3. Newly loaded data is uploaded to cloud storage

### Warehouse Schema (Gold Layer — Star Schema)

Dimension tables: `dim_date`, `dim_student`, `dim_course`, `dim_professor`, `dim_department`, `dim_semester`, `dim_course_offering`, `dim_assessment`

Fact tables: `fact_attendance`, `fact_assessment_result`

### Pipelines & Automation

Built using Azure Data Factory / Synapse-style pipelines and triggers:

- **Bronze trigger pipeline** — Watches for new/changed files landing in the Bronze folder, captures the file path/name and logs it (with upload date and pending/done status) to a Delta Lake table
- **Bronze → Silver pipeline** — Runs on a schedule or manually; loads pending files from the Delta Lake tracking table, then iterates through each file (ForEach) to run the transformation notebook, marking each as done and recording the output path in a `latest_files` Delta table
- **Silver trigger pipeline** — Watches for changes in the Silver folder
- **Silver → Gold pipeline** — Same pattern as Bronze → Silver: loads pending tables and transforms each into the curated star schema

## Machine Learning

A regression model predicts each student's expected performance score based on features such as current GPA, attendance rate, and credits earned. Predictions are surfaced back to students (e.g., predicted score, forecasted GPA trend) and stored in the `student_performance` table for downstream use in dashboards and intervention alerts.

## Dashboards

Two main dashboard experiences are included:

- **Student Hub (Student Portal)** — Personal dashboard showing predicted score, current GPA, credits earned, attendance rate, a performance & forecast chart, ML prediction gauge, semester GPA trend, and quick stats
- **Power BI (Business/Institutional View)** — Institution-wide dashboards covering % students at risk, average GPA, attendance/absence rate, average score by department/course/professor, session status breakdown, and student demographics (e.g., students at risk by gender)

## Tech Stack

- **Backend:** REST API (Python/FastAPI-style), relational database (SQL)
- **Cloud & Data Engineering:** Microsoft Azure (Blob Storage, synapse data pipelines, Delta Lake, notebooks)
- **Machine Learning:** Regression-based performance prediction
- **BI & Visualization:** Power BI

