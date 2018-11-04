FROM python:3.7-alpine
LABEL maintainer="Jean-Baptiste Martin <jeanbapt.martin@gmail.com>"

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libxml2-dev libxslt-dev \
    && pip install --no-cache-dir -r /usr/src/app/requirements.txt \
    && apk del .build-deps

COPY . /usr/src/app

WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
