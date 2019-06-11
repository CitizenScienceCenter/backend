#!/bin/sh

docker-compose -f ../docker-compose.test.yml up -d db
docker-compose -f ../docker-compose.test.yml up cccs-connexion
docker-compose -f ../docker-compose.test.yml down
