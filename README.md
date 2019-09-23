# CCCS Backend

[![Join the chat at https://gitter.im/CitizenScienceCenter/backend](https://badges.gitter.im/CitizenScienceCenter/backend.svg)](https://gitter.im/CitizenScienceCenter/backend?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Flask based OpenAPI (3) supported backend with a Postgres backend.

Current implementation holds a basic implementation with an API inspired by that of Pybossa. Basic auth is currently included.

## Running

* Ensure the correct `env` file has been symlinked to `.env`.

OR

* run `make ENVIRON=docker activate` to symlink `envs/docker.env`
* `make start` or `make start_service`

NOTE: starting as as service means that the processs is daemonized immediately and you must attach to the running container in order to debug (unless you redirect logs)

* `make stop` and `make clean`

### Testing

`make test`


## Resolving your spec

Here we use the [Speccy](https://github.com/wework/speccy) tool which requires npm (the docker file can also resolve it for you in the build steps)

`speccy resolve ./openapi/oapi.yaml -o ./oapi/cc.yaml`


### .env Contents

```env
CC_PORT=8080
ENV=local

HOST=https://api.citizenscience.ch
SWAGGER_URL=${HOST}/api/v3/openapi.json

SWAGGER_DIR=openapi/
SWAGGER_FILE=cc.yaml

SECRET_KEY=SUPES_SECRET987

PG_USER=YOURUSER
PG_PASSWORD=YOURPWD
PG_DB=cs
PG_HOST=0.0.0.0
DB_URI=postgresql://${PG_USER}:${PG_PASSWORD}@${PG_HOST}/${PG_DB}?sslmode=disable

COMPOSE_FILE=docker-compose.yml

SMTP_ADDR=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=

# DB will always be called `cs`
```

## Generate SDKs

Requires [swagger-codegen](https://swagger.io/swagger-codegen/).

### Example: Python

`swagger-codegen generate -i ./swagger/swagger.yaml -l python -o ./sdk/python`

## TODO

* [ ] Oauth support
* [ ] Generate E-R diagram
* [ ] Ownership handling
* [ ] Android/iOS client SDK generation
* [x] Reduce NoContent responses
* [x] Auth decorator
