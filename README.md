# 💳 Credit Card Risk Prediction System (End-to-End MLOps)

A production-grade Machine Learning system designed to predict credit card default risk. This project demonstrates a complete **End-to-End MLOps Pipeline**, from data ingestion to real-time monitoring.

## 🚀 Features
* **Full Pipeline:** Automated data ingestion, transformation, and model inference.
* **Model Serving:** Fast and asynchronous API using **FastAPI**.
* **Containerization:** Fully Dockerized environment for consistent deployment.
* **Observability:** Integrated with **Prometheus** to monitor API performance and prediction metrics.
* **CI/CD:** Automated builds and testing via **GitHub Actions**.

## 🛠 Tech Stack
* **Language:** Python 3.11
* **ML Frameworks:** Scikit-learn, LightGBM, XGBoost
* **API & Web:** FastAPI, Jinja2
* **DevOps & Monitoring:** Docker, Docker Compose, Prometheus, GitHub Actions
* **Data Versioning:** DVC (Data Version Control)

## 🏗 Project Structure
```text
├── artifacts/           # Model weights (model.joblib, preprocessor.joblib) and .dvc files
├── src/                 # Source code for pipelines and components
├── templates/           # Web UI files
├── .github/workflows/   # CI/CD automation
├── app.py               # FastAPI main application
├── docker-compose.yaml  # Multi-container orchestration
└── prometheus.yml       # Monitoring configuration
