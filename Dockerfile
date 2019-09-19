FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED 1
ARG ENV
ARG OUTPUT_SWAGGER
RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /code/
RUN rm -rf /code/__pycache__
RUN rm -rf /code/test/__pycache__
# COPY --from=0 /swagger/swagger_complete.yaml /code/swagger/swagger_complete.yaml
CMD python app.py

EXPOSE 8080
