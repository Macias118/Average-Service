FROM python:3.6

MAINTAINER Maciej Ruciński maciej.rucinski118@gmail.com

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
