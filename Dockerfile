FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
   libgomp1 \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

COPY . /app

ENV PYTHONPATH=/app
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -e . 

RUN python pipeline/training_pipeline.py

EXPOSE 5001

CMD ["python","application.py"]
