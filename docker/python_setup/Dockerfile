FROM python:3.9.17-alpine3.18

RUN apk add build-base=0.5-r3 --no-cache

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN rm -rf requirements.txt
