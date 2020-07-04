FROM postgres:latest

RUN apt-get update

ENV POSTGRES_DB image_microservice_test
ENV POSTGRES_USER db_user
ENV POSTGRES_PASSWORD 123456

COPY dump.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 5432