FROM quay.io/goswagger/swagger
ARG SW_ENV
WORKDIR /expand/
COPY swagger/ /expand/
RUN echo $SW_ENV
RUN swagger expand /expand/$SW_ENV > /expand/swagger_complete.yaml
RUN swagger validate /expand/swagger_complete.yaml


FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
COPY --from=0 /expand/swagger_complete.yaml /code/swagger/swagger_complete.yaml

