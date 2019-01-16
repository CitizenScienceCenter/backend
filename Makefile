include .env
export

export ENVFILE=.env

.PHONY: all
all:
		clean

.PHONY: clean
clean:
		docker-compose -f ${COMPOSE_FILE} rm
		-rm .env

.PHONY: test

.PHONY: start
start:
		git secret reveal -f
		docker-compose up --build --force-recreate

.PHONY: start_service
start_service:
		git secret reveal -f
		docker-compose -f ${COMPOSE_FILE} up --build --force-recreate -d

.PHONYL: stop
stop:
		docker-compose -f ${COMPOSE_FILE} down
		-rm .env

