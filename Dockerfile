#syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update -y \
    && apt-get upgrade -y pip \
    && pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . /code/