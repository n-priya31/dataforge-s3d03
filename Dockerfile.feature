FROM python:3.11-slim

WORKDIR /app
COPY app/feature_engineering.py /app/feature_engineering.py

ENV INPUT_PATH=/data/transformed_report.json
ENV OUTPUT_PATH=/data/feature_report.json

CMD ["python", "feature_engineering.py"]
