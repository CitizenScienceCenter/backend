# CCCS Backend

[![Join the chat at https://gitter.im/CitizenScienceCenter/backend](https://badges.gitter.im/CitizenScienceCenter/backend.svg)](https://gitter.im/CitizenScienceCenter/backend?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Flask based OpenAPI (3) supported backend with a Postgres backend.

Current implementation holds a basic implementation with an API inspired by that of Pybossa. Basic auth is currently included.

## Stack

We use Connexion as the **API Server**, based on Flask and you can find the API files in the `openapi` folder.

The **database** backend is PostgreSQL and the Docker Compose option allows you to choose an external DB or bring one up within the Compose file.

**File storage** can also be on the API server, or you can use Minio (an S3 clone). Support for direct uploads is coming in the near future.

## Running

* Ensure the correct `env` file has been symlinked to `.env`.

OR

* `make start` or `make start_bg`

NOTE: starting as `bg` means that the processs is daemonized immediately and you must attach to the running container in order to debug (unless you redirect logs)

* `make stop` and `make clean`

### Testing

`make test`


## Resolving your spec

Here we use the [Speccy](https://github.com/wework/speccy) tool which requires npm (the docker file can also resolve it for you in the build steps)

`speccy resolve ./openapi/oapi.yaml -o ./oapi/cc.yaml`


### .env Contents

```env
CC_PORT=8080
ENV=dev

HOST=https://api.citizenscience.ch
OAPI_URL=${HOST}/v3/openapi.json

OAPI_FILE=cc.yaml

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
```

## Generate SDKs

Requires [swagger-codegen](https://swagger.io/swagger-codegen/).

### Example: Python

`swagger-codegen generate -i ./swagger/swagger.yaml -l python -o ./sdk/python`

## TODO

* [ ] Oauth support
* [ ] Generate E-R diagram
* [x] Ownership handling
* [ ] Android/iOS client SDK generation
* [x] Reduce NoContent responses
* [x] Auth decorator
