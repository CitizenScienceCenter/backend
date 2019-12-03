from flask import Response, jsonify
import json


class ResponseHandler:

    mimetype = "application/json"
    body_key = "data"

    def __init__(
        self, status_code, msg, mimetype=None, body=None, ok=True
    ):
        self.body = {"code": status_code, "msg": msg, "ok": ok}
        self.code = status_code
        self.mimetype = self.mimetype
        if ok is False:
            self.body["err"] = msg
        if body is not None:
            self.body['data'] = body

    def set_body(self, body):
        self.body[self.body_key] = body

    def set_val(self, k, v):
        self.body[k] = v

    def send(self):
        return jsonify(self.body), self.code
