FROM postgres:11.5-alpine

ENV PG_USER $PG_USER

COPY scripts/pg/install_pgcrypto.sh /docker-entrypoint-initdb.d/
