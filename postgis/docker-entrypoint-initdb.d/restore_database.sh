#! /bin/bash

pg_restore -U postgres -d postgres -1 /docker-entrypoint-initdb.d/dump/nyc_data.backup