# CCCS Backend

[![Join the chat at https://gitter.im/CitizenScienceCenter/backend](https://badges.gitter.im/CitizenScienceCenter/backend.svg)](https://gitter.im/CitizenScienceCenter/backend?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Flask based OpenAPI (2) supported backend with a Postgres backend.

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

NOTE: This requires that port 5432 is available on your system. You can change this in the Makefile but this port **MUST** be fixed at 5432 for CI.


### .env Contents

```env
ENV=local # environment variable
CC_PORT=9000 
SW_ENV=swagger.yaml # swagger file to build from
DB_URI=postgresql://testing:testing@localhost/testcs?sslmode=disable
HOST=http://0.0.0.0:8081 # host for frontend
DEBUG=True
SWAGGER_DIR=swagger/
SWAGGER_FILE=swagger_complete.yaml # Swagger file to  pass to main app
SECRET_KEY=SUPES_SECRET987 # Secret key for sessions
COMPOSE_FILE=docker-compose.dev.yml # Docker compose file
PG_USER=testing # DB user
PG_PASSWORD=testing # DB pwd

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
* [ ] Reduce NoContent responses
* [x] Auth decorator
