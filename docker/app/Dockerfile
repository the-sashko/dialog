FROM python:3.9.17-alpine3.18

RUN apk add build-base

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN make test

ENTRYPOINT ["make run"]

CMD ["make run"]
