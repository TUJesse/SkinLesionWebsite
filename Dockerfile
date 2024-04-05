FROM python:3.11-slim
LABEL authors="jesse"

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev

COPY requirments.txt ./
COPY staticfiles ./
RUN pip install -r ./requirments.txt

COPY . .

EXPOSE 8000