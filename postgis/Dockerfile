# https://github.com/docker-library/docs/blob/master/postgres/README.md

FROM postgis/postgis:15-master
RUN apt-get update

COPY ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d