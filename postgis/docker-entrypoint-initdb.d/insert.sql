CREATE USER django WITH PASSWORD '7311';
CREATE DATABASE django;
ALTER DATABASE django OWNER TO django;

CREATE USER entity_framework WITH PASSWORD '7311';
CREATE DATABASE entity_framework;
ALTER ROLE entity_framework SUPERUSER;
ALTER DATABASE entity_framework OWNER TO entity_framework;

CREATE USER gisib WITH PASSWORD '7311' SUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN;
CREATE DATABASE gisib;
ALTER DATABASE gisib OWNER TO gisib;