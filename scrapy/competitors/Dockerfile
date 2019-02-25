FROM python:3.7-alpine3.9

RUN apk update && \
    apk add --no-cache \
    gcc \
    linux-headers \
    musl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    python3-dev \
    python3

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

ADD . /opt/competitors

RUN chmod +x /opt/competitors/run.sh

WORKDIR /opt/competitors

CMD touch /var/log/cron.log && cron && env > /root/env.sh && tail -f /var/log/cron.log