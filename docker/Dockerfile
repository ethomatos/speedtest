# Dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl speedtest-cli

WORKDIR /app
COPY speedtest.py .
# Install packages and verify installation
RUN pip install --no-cache-dir datadog

CMD ["python", "speedtest.py"]
