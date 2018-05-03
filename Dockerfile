FROM python:3.6
ADD . /cccs
WORKDIR /cccs
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main 9.5' > /etc/apt/sources.list.d/postgresql.list \
  && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && apt-get update -y \
  && apt-get install -y postgresql-9.5 postgresql-contrib-9.5 \
  && apt-get install sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]