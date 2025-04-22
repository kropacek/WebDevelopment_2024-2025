FROM python:3.10

WORKDIR /django_core

RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt
