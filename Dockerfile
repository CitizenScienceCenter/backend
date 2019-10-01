FROM python:3.7-alpine
RUN apk add build-base
RUN apk add postgresql-dev
RUN apk add libffi-dev
ENV PYTHONUNBUFFERED 1
ENV CC_PORT 9000
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN virtualenv env; source env/bin/activate
ADD requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /code/
EXPOSE 9000:9000
