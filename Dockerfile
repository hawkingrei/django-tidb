FROM ubuntu:latest

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    python3 \
    python3-dev \
    python3-pip \
    build-essential \
    git \
    binutils \
    mysql-client \
    libmysqlclient-dev \
    libmemcached-dev \
    curl

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN curl -s https://tiup-mirrors.pingcap.com/tidb-v5.1.0-linux-amd64.tar.gz | tar zxvf -

ADD . /django-tidb
RUN chmod 755 /django-tidb/run_testing_worker.py
WORKDIR /django-tidb
ENTRYPOINT ./run_testing_worker.py
