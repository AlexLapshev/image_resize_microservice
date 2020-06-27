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

--
-- Name: images; Type: TABLE; Schema: public; Owner: db_user
--
CREATE ROLE db_user WITH LOGIN PASSWORD '123456';


CREATE TABLE public.images (
    image_id integer NOT NULL,
    image_path character varying,
    image_status integer
);


ALTER TABLE public.images OWNER TO db_user;

--
-- Name: images_image_id_seq; Type: SEQUENCE; Schema: public; Owner: db_user
--

CREATE SEQUENCE public.images_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_image_id_seq OWNER TO db_user;

--
-- Name: images_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db_user
--

ALTER SEQUENCE public.images_image_id_seq OWNED BY public.images.image_id;


--
-- Name: status; Type: TABLE; Schema: public; Owner: db_user
--

CREATE TABLE public.status (
    status_id integer NOT NULL,
    status_name character varying
);


ALTER TABLE public.status OWNER TO db_user;



--
-- Name: status_status_id_seq; Type: SEQUENCE; Schema: public; Owner: db_user
--

CREATE SEQUENCE public.status_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_status_id_seq OWNER TO db_user;

--
-- Name: status_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: db_user
--

ALTER SEQUENCE public.status_status_id_seq OWNED BY public.status.status_id;


--
-- Name: images image_id; Type: DEFAULT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.images ALTER COLUMN image_id SET DEFAULT nextval('public.images_image_id_seq'::regclass);


--
-- Name: status status_id; Type: DEFAULT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.status ALTER COLUMN status_id SET DEFAULT nextval('public.status_status_id_seq'::regclass);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (image_id);


--
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (status_id);


--
-- Name: images images_image_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: db_user
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_image_status_fkey FOREIGN KEY (image_status) REFERENCES public.status(status_id);


INSERT INTO public.status (status_id, status_name)
VALUES
    (1, 'CREATED'),
    (2, 'IN_PROGRESS'),
    (3, 'SUCCESS');

--
-- PostgreSQL database dump complete
--

