FROM python:3.9.17-alpine3.18

COPY . /app
WORKDIR /app

RUN make test

ENTRYPOINT ["make run"]

CMD ["make run"]
