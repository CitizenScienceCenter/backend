from flask import Response, jsonify
import json

class ResponseHandler():

    mimetype = 'application/json'
    body_key = 'body'

    def __init__(self, status_code, msg, body_key=None, mimetype=None, body=None, ok=True):
        self.msg = {
            'code': status_code,
            'msg': msg,
            'ok': ok
        }
        self.code = status_code
        self.body_key = body_key
        self.mimetype = self.mimetype
        if body is not None:
            self.msg['body'] = body


    def set_body(self, body):
        self.msg['body'] = body

    def set_val(self, k, v):
        self.msg[k] = v

    def send(self):
        return jsonify(self.msg), self.code