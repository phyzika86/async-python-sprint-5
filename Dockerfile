FROM python:3.10-bullseye

WORKDIR ./opt/src

COPY requirements.txt /opt/src
RUN pip install -r requirements.txt
COPY src /opt/src