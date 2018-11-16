FROM python:3.6-slim

MAINTAINER Agung Wiyono <wiyonoagung1@gmail.com>

RUN apt-get update && apt-get install -qq -y \
	build-essential libpq-dev --no-install-recommends

RUN apt-get update

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["./boot.sh"]
