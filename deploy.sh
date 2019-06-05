#!/bin/bash

BRANCH=`git rev-parse --abbrev-ref HEAD | tr / _`
TAG=`git rev-parse --short HEAD`
REG=registry.citizenscience.ch
IMG=backend

URL=${REG}/${IMG}:${BRANCH}${TAG}

echo ${URL}

docker build -t ${URL} .
docker push ${URL}
