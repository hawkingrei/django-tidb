FROM ubuntu

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-dev python3-pip \
    build-essential git binutils mysql-client libmysqlclient-dev libmemcached-dev

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8