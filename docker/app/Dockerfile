FROM 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.1.0

COPY . /app

RUN rm -rf /app/docker
RUN rm /app/docker-compose.yml

WORKDIR /app

EXPOSE 80
EXPOSE 443

CMD [ "python", "-u", "src/app.py" ]

#FROM 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.1.0

#RUN pip3 install boto3==v1.28.30

#COPY . /app

#RUN cp /app/docker/app/cronfile /etc/cron.d/dialog_cron
#RUN chmod 0644 /etc/cron.d/dialog_cron
#RUN crontab /etc/cron.d/dialog_cron

#RUN rm -rf /app/docker
#RUN rm /app/docker-compose.yml

#WORKDIR /app

#EXPOSE 80
#EXPOSE 443

#CMD cron && python -u src/app.py
