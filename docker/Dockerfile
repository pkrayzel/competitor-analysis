FROM library/python:3.7-alpine3.9

RUN apk --update --no-cache add \
        build-base \
        libffi-dev \
        libxslt-dev \
        openssl-dev \
        gcc \
        wget \
        git \
        chromium \
        chromium-chromedriver \
    && rm -rf /var/cache/apk/*

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt \

ADD ./src /src

ENTRYPOINT []