-include .env
export

export ENVFILE=.env
DBEXIST := $(shell docker ps | grep -q testpg)

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
		ifeq ($(shell docker ps | grep -q testpg), )
		  docker run --name testpg -e POSTGRES_DB=testcs -e POSTGRES_USER=testing -e POSTGRES_PASSWORD=testing -p "6000:5432" -d postgres
		endif


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

