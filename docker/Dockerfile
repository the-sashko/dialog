FROM python:3.9.17-alpine3.18

RUN git clone https://github.com/the-sashko/dialog
WORKDIR /app
RUN pip install -r requirements.txt
RUN make install
RUN make test

ENTRYPOINT ["make run"]

CMD ["make run"]
