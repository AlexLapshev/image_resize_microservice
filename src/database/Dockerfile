FROM postgres:latest

ENV POSTGRES_PASSWORD 123456
ENV POSTGRES_DB image_microservice

COPY image_microservice_dump.sql /docker-entrypoint-initdb.d
