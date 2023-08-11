FROM python:3.9.17-alpine3.18

RUN apk add build-base=0.5-r3 --no-cahce

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
