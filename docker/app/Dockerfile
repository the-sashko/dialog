FROM 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

RUN apk add ffmpeg=6.0-r15 --no-cache

COPY . /app

RUN rm -rf /app/docker

WORKDIR /app

EXPOSE 80
EXPOSE 443

CMD [ "python", "./srs/app.py" ]

