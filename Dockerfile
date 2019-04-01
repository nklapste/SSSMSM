FROM python:3.6-stretch

LABEL maintainer="nklapste@ualberta.ca"

ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir ghast
RUN apt-get update
RUN apt-get install docker.io -y

ENTRYPOINT ["ssswms"]
