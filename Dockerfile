FROM ubuntu:16.04

FROM python:3.6.5

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD python /app/flask_api.py
