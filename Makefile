-include .env
export

.PHONY: spec swaggerui run
all:
		clean
		start

init:
	virtualenv env
	touch .env

reveal:
	git secret reveal -f

.PHONY: clean
clean:
		docker-compose -f ${COMPOSE_FILE} rm
		-rm .env

docs:
	sphinx-apidoc -o docs .

.PHONY: spec
spec:
	  speccy resolve openapi/oapi.yaml -o openapi/cc.yaml

.PHONY: localdb
localdb:
	 -docker kill backend-db
	 -docker rm backend-db
	 docker run --name backend-db -e POSTGRES_PASSWORD=testing -e POSTGRES_USER=testing -e POSTGRES_DB=testcs -d -p "5432:5432" postgres

services: spec localdb

local: services run

cfg = dev

.PHONY: run
run:
	ln -sf config/$(cfg).cfg .env
	python app.py

.PHONY: test
test:
		ln -sf config/test.cfg .env
		env/bin/python -m pytest test/*.py -s

.PHONY: env
env:
	ln -sf config/$(cfg).cfg .env

.PHONY: api
api:
	docker-compose up --build --force-recreate --no-deps -d api

.PHONY: start
docker:
		git secret reveal -f
		docker-compose up --build --force-recreate

.PHONY: start_service
daemon:
		git secret reveal -f
		docker-compose -f ${COMPOSE_FILE} up --build --force-recreate -d

.PHONY: stop
stop:
		docker-compose -f ${COMPOSE_FILE} down
		-rm .env

