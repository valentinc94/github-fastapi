FROM python:3.10
MAINTAINER Valentin Castillo <valentincc94m@gmail.com>

ARG target_env="local"
ENV TARGET_ENV=$target_env

RUN mkdir /backend /var/secrets
WORKDIR backend

RUN apt-get update \
    && apt-get install -y python3-dev musl-dev libxmlsec1-dev pkg-config


COPY ./requirements/ /backend/requirements/

RUN pip install -r /backend/requirements/${TARGET_ENV}.txt

COPY . .

RUN addgroup --gid 1000 docker \
    && adduser --gid 1000 --uid 1000 --disabled-password --gecos "" --quiet docker \
    && chown -R docker:docker /var/secrets /backend

USER docker
