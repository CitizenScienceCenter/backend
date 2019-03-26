# FROM quay.io/goswagger/swagger
# ARG SOURCE_SWAGGER
# ARG OUTPUT_SWAGGER
# WORKDIR /output/
# COPY . .
# RUN echo $SOURCE_SWAGGER
# RUN swagger expand swagger/$SOURCE_SWAGGER > /output/$OUTPUT_SWAGGER
# RUN swagger validate /output/$OUTPUT_SWAGGER

FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED 1
ARG CC_ENV
ARG OUTPUT_SWAGGER
RUN mkdir /code
WORKDIR /code
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD . /code/
RUN rm -rf /code/__pycache__
RUN rm -rf /code/test/__pycache__
# COPY --from=0 /swagger/swagger_complete.yaml /code/swagger/swagger_complete.yaml
