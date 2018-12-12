include ${ENVFILE}
export

.PHONY: all
all:
		clean

.PHONY: clean
clean:
		docker-compose -f ${COMPOSE_FILE} rm

.PHONY: test

.PHONY: start
start:
		git secret reveal -f
		-cp -f ${ENVFILE} .env
		docker-compose up --build --force-recreate

.PHONY: start_service
start_service:
		git secret reveal -f
		-cp -f ${ENVFILE} .env
		docker-compose -f ${COMPOSE_FILE} up --build --force-recreate -d

.PHONYL: stop
stop:
		docker-compose -f ${COMPOSE_FILE} down
		-rm .env

