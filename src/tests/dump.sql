--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.images (
    image_id integer NOT NULL,
    image_task_id character varying,
    image_path character varying
);


ALTER TABLE public.images OWNER TO db_user;


CREATE SEQUENCE public.images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_image_id_seq OWNER TO db_user;


ALTER SEQUENCE public.images_image_id_seq OWNED BY public.images.image_id;


ALTER TABLE ONLY public.images ALTER COLUMN image_id SET DEFAULT nextval('public.images_image_id_seq'::regclass);


ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (image_id);

INSERT INTO public.images (image_id, image_task_id, image_path)
VALUES (1, 'af90a559-14c2-4fd2-ad10-d1573b5195e0', '/app/src/tests/data_test/test.jpg');


