FROM alpine:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt autoremove -y && \
    apt-get install -y python3
RUN git clone
RUN cd /app
WORKDIR /app
RUN make install
RUN make test

ENTRYPOINT ["make run"]

CMD ["make run"]
