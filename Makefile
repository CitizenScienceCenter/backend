-include .env
export

export ENVFILE=.env

.PHONY: all
all:
		clean
		start

.PHONY: activate
activate:
		git secret reveal -f
		-rm .env
		ln -s envs/${ENVIRON}.env .env

.PHONY: clean
clean:
		docker-compose -f ${COMPOSE_FILE} rm
		-rm .env

.PHONY: test
test:
		ln -sf envs/test.env .env
		docker-compose -f docker-compose.test.yml up --build

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

