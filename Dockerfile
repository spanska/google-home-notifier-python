FROM tiangolo/uwsgi-nginx-flask:python3.6
MAINTAINER Jean-Baptiste Martin "jeanbapt.martin@gmail.com"

ENV LISTEN_PORT 8080
EXPOSE 8080

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
