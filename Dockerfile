FROM python:3.8.3-slim

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD /bin/bash

CMD python -m src.main