FROM python:3.9.17-alpine3.18

RUN apk add build-base=0.5-r3 --no-cache
RUN apk add linux-headers=6.3-r0 --no-cache
RUN apk add ffmpeg=6.0-r15 --no-cache

RUN pip3 install datetime==v5.2
RUN pip3 install grpcio==v1.57.0
RUN pip3 install gtts==v2.3.2
RUN pip3 install numpy==v1.25.2
RUN pip3 install openai==v0.27.8
RUN pip3 install pillow==v10.0.0
RUN pip3 install pydub==v0.25.1
RUN pip3 install requests==v2.31.0
RUN pip3 install stability_sdk==v0.8.4
RUN pip3 install boto3==v1.28.30
