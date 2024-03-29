# syntax=docker/dockerfile:1.3
FROM python:3.11-alpine

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY . .

EXPOSE 8888

RUN pip install --no-cache-dir --upgrade -r requirements.txt