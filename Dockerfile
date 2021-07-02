FROM ubuntu

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-dev python3-pip \
    build-essential git binutils mysql-client libmysqlclient-dev

# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8