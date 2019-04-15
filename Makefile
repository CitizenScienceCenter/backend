include .env
export

.PHONY: all
all:
		clean
		start

.PHONY: clean
clean:
		docker-compose -f ${COMPOSE_FILE} rm
		-rm .env

.PHONY: test
test:
		ln -sf envs/test.env .env
		docker-compose -f docker-compose.test.yml up --build --force-recreate

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

