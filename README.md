# CCCS Connexions App

Flask based OpenAPI (2) supported backend with a Postgres backend.

Current implementation holds a basic implementation with an API inspired by that of Pybossa. No auth is currently included.

## Running

### Locally

* `virtualenv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
* Set connection settings and others in `config.py`
* `python app.py`

### Docker (with Docker Compose)

* `docker compose up`

## Generate SDKs

Requires [swagger-codegen](https://swagger.io/swagger-codegen/).

### Example: Python

`swagger-codegen generate -i ./swagger/swagger.yaml -l python -o ./sdk/python`

## TODO

* Oauth support
* Implement endpoints for:
  * submission
  * participant
* Generate E-R diagram
* Endpoint security
* Project deletion only by project owner
* Android/iOS client SDK generation
* Reduce NoContent responses
* Auth decorator
