FROM python:3.12.1-alpine

COPY ./flaskapp/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /app
COPY ./flaskapp /app

WORKDIR /app