FROM python:3.7

RUN mkdir /app/
WORKDIR /app/
ADD python/requirements.txt /app/
RUN pip install -r requirements.txt
ADD python/* /app/
