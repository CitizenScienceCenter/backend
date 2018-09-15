# CCCS Backend

Flask based OpenAPI (2) supported backend with a Postgres backend.

Current implementation holds a basic implementation with an API inspired by that of Pybossa. Basic auth is currently included.

## Running

### Locally

* `virtualenv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
* Set connection settings and others in `config.py`
* `python app.py`

### Docker (with Docker Compose)

* Set connexion settings in config/<env>.py
* `docker compose up`

## Using

When it is running, port 8080 is exposed. You can use Nginx (or similar) to proxy through to this or access it through this port. You can access a hosted version [here](https://api.citizenscience.ch)

## Generate SDKs

Requires [swagger-codegen](https://swagger.io/swagger-codegen/).

### Example: Python

`swagger-codegen generate -i ./swagger/swagger.yaml -l python -o ./sdk/python`

## TODO

* Oauth support
* Generate E-R diagram
* Ownserhip handling
* Android/iOS client SDK generation
* Reduce NoContent responses
* Auth decorator
