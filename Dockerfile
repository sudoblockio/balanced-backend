FROM python:3.10-slim-buster

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME:-api}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt:${PYTHONPATH}"

WORKDIR /opt

RUN pip install --upgrade pip
COPY ./requirements-$SERVICE_NAME.txt .
RUN pip install -r ./requirements-$SERVICE_NAME.txt

COPY balanced_backend ./balanced_backend

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

RUN useradd -m icon
USER icon

ENTRYPOINT ./entrypoint.sh $SERVICE_NAME
