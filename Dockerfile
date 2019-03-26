FROM quay.io/goswagger/swagger
ARG SOURCE_SWAGGER
ARG OUTPUT_SWAGGER
WORKDIR /expand/
COPY . .
RUN echo $SOURCE_SWAGGER
RUN swagger expand swagger/$SOURCE_SWAGGER > /expand/$OUTPUT_SWAGGER
RUN swagger validate /expand/$OUTPUT_SWAGGER

FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED 1
ARG CC_ENV
ARG OUTPUT_SWAGGER
RUN mkdir /code
WORKDIR /code
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD . /code/
<<<<<<< HEAD
COPY --from=0 /expand/$OUTPUT_SWAGGER /code/$OUTPUT_SWAGGER
=======
RUN rm -rf /code/__pycache__
RUN rm -rf /code/test/__pycache__
COPY --from=0 /expand/swagger_complete.yaml /code/swagger/swagger_complete.yaml
>>>>>>> develop
