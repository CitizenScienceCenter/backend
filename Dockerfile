 FROM python:3.6.6-stretch
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN apt update && apt install -y python3-dev libpython3-dev
 RUN pip3 install -r requirements.txt
 ADD . /code/

