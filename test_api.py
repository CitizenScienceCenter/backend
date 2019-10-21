# test_api.py
import requests
import schemathesis

schema = schemathesis.from_uri("http://0.0.0.0:9000/v3/openapi.json")

@schema.parametrize()
def test_no_server_errors(case):
    # `requests` will make an appropriate call under the hood
    response = case.call()
    assert response.status_code < 500
