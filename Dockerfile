FROM python:3.12-slim
LABEL maintainer="chebukin404@gmail.com"

WORKDIR seejet-tracker/

ENV PYTHONUNNBUFFERED 1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    jet_user

RUN chown -R jet_user /files/media
RUN chmod -R 755 /files/media

USER jet_user
