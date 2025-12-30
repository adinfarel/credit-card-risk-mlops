FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --default-timeout=1000 --upgrade -r /app/requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV MLFLOW_TRACKING_URI=sqlite://mlflow.db

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
