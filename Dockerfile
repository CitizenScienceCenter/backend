FROM quay.io/goswagger/swagger
WORKDIR /expand/
ARG SWAGGER_ENV
COPY . .
RUN echo ${SWAGGER_ENV}
RUN swagger expand swagger/${SWAGGER_ENV} > /expand/swagger_complete.yaml
RUN swagger validate /expand/swagger_complete.yaml

FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED 1
ARG CC_ENV
RUN mkdir /code
WORKDIR /code
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD . /code/
RUN rm -rf /code/__pycache__
RUN rm -rf /code/test/__pycache__
COPY --from=0 /expand/swagger_complete.yaml /code/swagger/swagger_complete.yaml
