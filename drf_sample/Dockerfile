FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y \
                       curl \
                       git \
                       libpq-dev \
                       python3-pip \
                       python3.5 \
                       uwsgi uwsgi-plugin-python3

RUN update-alternatives --install /usr/bin/python3 python3.5 /usr/bin/python3.5 0

WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

ADD . /code
WORKDIR /code
