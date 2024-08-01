# Dockerfile
FROM python

WORKDIR /app

COPY export-metrics.py /app/
RUN pip install prometheus_client psycopg2

CMD ["python", "export-metrics.py"]
