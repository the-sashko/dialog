FROM python3:latest

RUN git clone https://github.com/the-sashko/dialog
RUN cd /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN make install
RUN make test

ENTRYPOINT ["make run"]

CMD ["make run"]
