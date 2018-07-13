FROM tiangolo/uwsgi-nginx-flask:python3.6
MAINTAINER Jean-Baptiste Martin "jeanbapt.martin@gmail.com"

ENV LISTEN_PORT 5000
EXPOSE 5000

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
