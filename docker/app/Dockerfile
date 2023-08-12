FROM 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

COPY . /app
WORKDIR /app

RUN make clean

RUN rm -rf /app/.git
RUN rm -rf /app/logs/*
RUN rm /app/data/db.sqlite3

RUN make parse

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["make run"]

CMD ["make run"]
