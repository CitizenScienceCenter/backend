#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$PG_USER" <<-EOSQL
create extension pgcrypto;
EOSQL
