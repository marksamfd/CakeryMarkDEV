--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: Cakery_DB1_Populated; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "Cakery_DB1_Populated";


ALTER SCHEMA "Cakery_DB1_Populated" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin (
    adminemail character varying(255) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.admin OWNER TO postgres;

--
-- Name: bakeryuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bakeryuser (
    bakeryemail character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    firstname character varying(255),
    lastname character varying(255),
    phonenum character varying(15),
    addresstext text,
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.bakeryuser OWNER TO postgres;

--
-- Name: cakelayer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cakelayer (
    layerid integer NOT NULL,
    customcakeid integer,
    level integer NOT NULL,
    flavor character varying(255),
    innerfilling character varying(255),
    nuts character varying(255)
);


ALTER TABLE public.cakelayer OWNER TO postgres;

--
-- Name: cakelayer_layerid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cakelayer_layerid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cakelayer_layerid_seq OWNER TO postgres;

--
-- Name: cakelayer_layerid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cakelayer_layerid_seq OWNED BY public.cakelayer.layerid;


--
-- Name: cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart (
    cartid integer NOT NULL,
    customeremail character varying(255) NOT NULL
);


ALTER TABLE public.cart OWNER TO postgres;

--
-- Name: cart_cartid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_cartid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_cartid_seq OWNER TO postgres;

--
-- Name: cart_cartid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_cartid_seq OWNED BY public.cart.cartid;


--
-- Name: cartitems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cartitems (
    cartitemid integer NOT NULL,
    cartid integer NOT NULL,
    productid integer,
    customcakeid integer,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.cartitems OWNER TO postgres;

--
-- Name: cartitems_cartitemid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cartitems_cartitemid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cartitems_cartitemid_seq OWNER TO postgres;

--
-- Name: cartitems_cartitemid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cartitems_cartitemid_seq OWNED BY public.cartitems.cartitemid;


--
-- Name: customcake; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customcake (
    customcakeid integer NOT NULL,
    numlayers integer NOT NULL,
    sugarpaste character varying(255),
    coating character varying(255),
    topping character varying(255)
);


ALTER TABLE public.customcake OWNER TO postgres;

--
-- Name: customcake_customcakeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customcake_customcakeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customcake_customcakeid_seq OWNER TO postgres;

--
-- Name: customcake_customcakeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customcake_customcakeid_seq OWNED BY public.customcake.customcakeid;


--
-- Name: customeruser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customeruser (
    customeremail character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    firstname character varying(255),
    lastname character varying(255),
    phonenum character varying(15),
    addressgooglemapurl text,
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.customeruser OWNER TO postgres;

--
-- Name: delivery_assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.delivery_assignments (
    id integer NOT NULL,
    deliveryemail character varying(255),
    orderid integer
);


ALTER TABLE public.delivery_assignments OWNER TO postgres;

--
-- Name: delivery_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.delivery_assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.delivery_assignments_id_seq OWNER TO postgres;

--
-- Name: delivery_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.delivery_assignments_id_seq OWNED BY public.delivery_assignments.id;


--
-- Name: deliveryuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deliveryuser (
    deliveryemail character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    firstname character varying(255),
    lastname character varying(255),
    phonenum character varying(15),
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.deliveryuser OWNER TO postgres;

--
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    productid integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2),
    category character varying(255),
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- Name: inventory_productid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.inventory_productid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventory_productid_seq OWNER TO postgres;

--
-- Name: inventory_productid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.inventory_productid_seq OWNED BY public.inventory.productid;


--
-- Name: orderitems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orderitems (
    orderitemid integer NOT NULL,
    orderid integer,
    productid integer,
    customcakeid integer,
    quantity integer NOT NULL,
    priceatorder numeric(10,2)
);


ALTER TABLE public.orderitems OWNER TO postgres;

--
-- Name: orderitems_orderitemid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orderitems_orderitemid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orderitems_orderitemid_seq OWNER TO postgres;

--
-- Name: orderitems_orderitemid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orderitems_orderitemid_seq OWNED BY public.orderitems.orderitemid;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    orderid integer NOT NULL,
    customeremail character varying(255),
    deliveryemail character varying(255),
    totalprice numeric(10,2),
    status character varying(50),
    orderdate timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deliverydate timestamp without time zone
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_orderid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_orderid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_orderid_seq OWNER TO postgres;

--
-- Name: orders_orderid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_orderid_seq OWNED BY public.orders.orderid;


--
-- Name: payment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment (
    paymentid integer NOT NULL,
    orderid integer NOT NULL,
    deposit numeric(10,2) NOT NULL,
    restofprice numeric(10,2) NOT NULL,
    paymentdate timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payment OWNER TO postgres;

--
-- Name: payment_paymentid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payment_paymentid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payment_paymentid_seq OWNER TO postgres;

--
-- Name: payment_paymentid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payment_paymentid_seq OWNED BY public.payment.paymentid;


--
-- Name: review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review (
    reviewid integer NOT NULL,
    orderid integer,
    customeremail character varying(255),
    rating integer,
    createdat timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT review_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.review OWNER TO postgres;

--
-- Name: review_reviewid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.review_reviewid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_reviewid_seq OWNER TO postgres;

--
-- Name: review_reviewid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.review_reviewid_seq OWNED BY public.review.reviewid;


--
-- Name: voucher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.voucher (
    vouchercode character varying(255) NOT NULL,
    discountpercentage numeric(5,2) NOT NULL
);


ALTER TABLE public.voucher OWNER TO postgres;

--
-- Name: cakelayer layerid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cakelayer ALTER COLUMN layerid SET DEFAULT nextval('public.cakelayer_layerid_seq'::regclass);


--
-- Name: cart cartid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart ALTER COLUMN cartid SET DEFAULT nextval('public.cart_cartid_seq'::regclass);


--
-- Name: cartitems cartitemid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartitems ALTER COLUMN cartitemid SET DEFAULT nextval('public.cartitems_cartitemid_seq'::regclass);


--
-- Name: customcake customcakeid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customcake ALTER COLUMN customcakeid SET DEFAULT nextval('public.customcake_customcakeid_seq'::regclass);


--
-- Name: delivery_assignments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_assignments ALTER COLUMN id SET DEFAULT nextval('public.delivery_assignments_id_seq'::regclass);


--
-- Name: inventory productid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory ALTER COLUMN productid SET DEFAULT nextval('public.inventory_productid_seq'::regclass);


--
-- Name: orderitems orderitemid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderitems ALTER COLUMN orderitemid SET DEFAULT nextval('public.orderitems_orderitemid_seq'::regclass);


--
-- Name: orders orderid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN orderid SET DEFAULT nextval('public.orders_orderid_seq'::regclass);


--
-- Name: payment paymentid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment ALTER COLUMN paymentid SET DEFAULT nextval('public.payment_paymentid_seq'::regclass);


--
-- Name: review reviewid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review ALTER COLUMN reviewid SET DEFAULT nextval('public.review_reviewid_seq'::regclass);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin (adminemail, password) FROM stdin;
admin@cakery_admin.com	adminPass123
\.


--
-- Data for Name: bakeryuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bakeryuser (bakeryemail, password, firstname, lastname, phonenum, addresstext, createdat) FROM stdin;
mohamed.ehab@cakery_baker.com	passMohamed	Mohamed	Ehab	0223344556	123 Bakery Street, City	2024-11-23 01:57:30.306462
ahmad.fouda@cakery_baker.com	passAhmad	Ahmad	Fouda	0334455667	456 Pastry Avenue, City	2024-11-23 01:57:30.306462
\.


--
-- Data for Name: cakelayer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cakelayer (layerid, customcakeid, level, flavor, innerfilling, nuts) FROM stdin;
1	1	1	Red Velvet	Cream Cheese	Pecans
2	1	2	Lemon	Lemon Curd	Almonds
\.


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart (cartid, customeremail) FROM stdin;
1	anas.ahmad@gmail.com
2	mark.samuel@gmail.com
3	tasneem.mohamed@gmail.com
\.


--
-- Data for Name: cartitems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cartitems (cartitemid, cartid, productid, customcakeid, quantity, price) FROM stdin;
2	1	\N	1	1	60.00
3	2	3	\N	3	4.50
4	3	1	\N	1	25.00
6	1	3	\N	2	4.50
8	1	2	\N	2	3.00
\.


--
-- Data for Name: customcake; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customcake (customcakeid, numlayers, sugarpaste, coating, topping) FROM stdin;
1	2	Fondant	Buttercream	Mixed Berries
\.


--
-- Data for Name: customeruser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customeruser (customeremail, password, firstname, lastname, phonenum, addressgooglemapurl, createdat) FROM stdin;
anas.ahmad@gmail.com	passAnas	Anas	Ahmad	0123456789	https://maps.google.com/?q=AnasAddress	2024-11-23 01:58:44.668676
mark.samuel@gmail.com	passMark	Mark	Samuel	0987654321	https://maps.google.com/?q=MarkAddress	2024-11-23 01:58:44.668676
tasneem.mohamed@gmail.com	passTasneem	Tasneem	Mohamed	0112233445	https://maps.google.com/?q=TasneemAddress	2024-11-23 01:58:44.668676
\.


--
-- Data for Name: delivery_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.delivery_assignments (id, deliveryemail, orderid) FROM stdin;
1	john.doe@cakery_delivery.com	2
\.


--
-- Data for Name: deliveryuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deliveryuser (deliveryemail, password, firstname, lastname, phonenum, createdat) FROM stdin;
sarah.lee@cakery_delivery.com	passSarah	Sarah	Lee	0556677889	2024-11-23 01:58:26.971613
john.doe@cakery_delivery.com	passJohn	John	Doe	0445566778	2024-11-23 01:58:26.971613
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory (productid, name, description, price, category, createdat) FROM stdin;
1	Chocolate Cake	Rich and moist chocolate cake	25.00	Cake	2024-11-23 02:01:50.13918
2	Vanilla Cupcake	Classic vanilla cupcake with buttercream frosting	3.00	Cupcake	2024-11-23 02:01:50.13918
3	Strawberry Tart	Fresh strawberries on a crispy tart base	4.50	Tart	2024-11-23 02:01:50.13918
\.


--
-- Data for Name: orderitems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orderitems (orderitemid, orderid, productid, customcakeid, quantity, priceatorder) FROM stdin;
1	1	2	\N	4	3.00
2	1	\N	1	1	60.00
3	2	3	\N	3	4.50
4	3	1	\N	1	25.00
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (orderid, customeremail, deliveryemail, totalprice, status, orderdate, deliverydate) FROM stdin;
3	tasneem.mohamed@gmail.com	john.doe@cakery_delivery.com	25.00	Out for Delivery	2024-11-23 02:07:02.387941	\N
1	anas.ahmad@gmail.com	john.doe@cakery_delivery.com	72.00	Prepared	2024-11-23 02:06:47.172561	\N
2	mark.samuel@gmail.com	sarah.lee@cakery_delivery.com	13.50	Prepared	2024-11-23 02:06:57.586371	\N
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment (paymentid, orderid, deposit, restofprice, paymentdate) FROM stdin;
1	1	30.00	42.00	2024-11-23 02:07:36.344532
2	2	13.50	0.00	2024-11-23 02:07:43.088481
3	3	22.50	0.00	2024-11-23 02:07:47.606528
\.


--
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.review (reviewid, orderid, customeremail, rating, createdat) FROM stdin;
1	1	anas.ahmad@gmail.com	5	2024-11-23 02:08:52.708337
2	2	mark.samuel@gmail.com	4	2024-11-23 02:08:57.532189
3	3	tasneem.mohamed@gmail.com	5	2024-11-23 02:09:03.869458
\.


--
-- Data for Name: voucher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.voucher (vouchercode, discountpercentage) FROM stdin;
WELCOME10	10.00
SUMMER15	15.00
\.


--
-- Name: cakelayer_layerid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cakelayer_layerid_seq', 2, true);


--
-- Name: cart_cartid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_cartid_seq', 3, true);


--
-- Name: cartitems_cartitemid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cartitems_cartitemid_seq', 8, true);


--
-- Name: customcake_customcakeid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customcake_customcakeid_seq', 1, true);


--
-- Name: delivery_assignments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.delivery_assignments_id_seq', 1, true);


--
-- Name: inventory_productid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.inventory_productid_seq', 3, true);


--
-- Name: orderitems_orderitemid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orderitems_orderitemid_seq', 4, true);


--
-- Name: orders_orderid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_orderid_seq', 3, true);


--
-- Name: payment_paymentid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payment_paymentid_seq', 3, true);


--
-- Name: review_reviewid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.review_reviewid_seq', 3, true);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (adminemail);


--
-- Name: bakeryuser bakeryuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bakeryuser
    ADD CONSTRAINT bakeryuser_pkey PRIMARY KEY (bakeryemail);


--
-- Name: cakelayer cakelayer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cakelayer
    ADD CONSTRAINT cakelayer_pkey PRIMARY KEY (layerid);


--
-- Name: cart cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (cartid);


--
-- Name: cartitems cartitems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartitems
    ADD CONSTRAINT cartitems_pkey PRIMARY KEY (cartitemid);


--
-- Name: customcake customcake_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customcake
    ADD CONSTRAINT customcake_pkey PRIMARY KEY (customcakeid);


--
-- Name: customeruser customeruser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customeruser
    ADD CONSTRAINT customeruser_pkey PRIMARY KEY (customeremail);


--
-- Name: delivery_assignments delivery_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_assignments
    ADD CONSTRAINT delivery_assignments_pkey PRIMARY KEY (id);


--
-- Name: deliveryuser deliveryuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deliveryuser
    ADD CONSTRAINT deliveryuser_pkey PRIMARY KEY (deliveryemail);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (productid);


--
-- Name: orderitems orderitems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderitems
    ADD CONSTRAINT orderitems_pkey PRIMARY KEY (orderitemid);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (orderid);


--
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (paymentid);


--
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (reviewid);


--
-- Name: cart unique_customer_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT unique_customer_email UNIQUE (customeremail);


--
-- Name: inventory unique_name_category; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT unique_name_category UNIQUE (name, category);


--
-- Name: voucher voucher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.voucher
    ADD CONSTRAINT voucher_pkey PRIMARY KEY (vouchercode);


--
-- Name: cakelayer cakelayer_customcakeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cakelayer
    ADD CONSTRAINT cakelayer_customcakeid_fkey FOREIGN KEY (customcakeid) REFERENCES public.customcake(customcakeid);


--
-- Name: cart cart_customeremail_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_customeremail_fkey FOREIGN KEY (customeremail) REFERENCES public.customeruser(customeremail);


--
-- Name: cartitems cartitems_cartid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartitems
    ADD CONSTRAINT cartitems_cartid_fkey FOREIGN KEY (cartid) REFERENCES public.cart(cartid) ON DELETE CASCADE;


--
-- Name: cartitems cartitems_customcakeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartitems
    ADD CONSTRAINT cartitems_customcakeid_fkey FOREIGN KEY (customcakeid) REFERENCES public.customcake(customcakeid);


--
-- Name: cartitems cartitems_productid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cartitems
    ADD CONSTRAINT cartitems_productid_fkey FOREIGN KEY (productid) REFERENCES public.inventory(productid);


--
-- Name: delivery_assignments delivery_assignments_deliveryemail_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_assignments
    ADD CONSTRAINT delivery_assignments_deliveryemail_fkey FOREIGN KEY (deliveryemail) REFERENCES public.deliveryuser(deliveryemail) ON DELETE CASCADE;


--
-- Name: delivery_assignments delivery_assignments_orderid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.delivery_assignments
    ADD CONSTRAINT delivery_assignments_orderid_fkey FOREIGN KEY (orderid) REFERENCES public.orders(orderid) ON DELETE CASCADE;


--
-- Name: orders fk_orders_deliveryuser; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_orders_deliveryuser FOREIGN KEY (deliveryemail) REFERENCES public.deliveryuser(deliveryemail);


--
-- Name: orderitems orderitems_customcakeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderitems
    ADD CONSTRAINT orderitems_customcakeid_fkey FOREIGN KEY (customcakeid) REFERENCES public.customcake(customcakeid);


--
-- Name: orderitems orderitems_orderid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderitems
    ADD CONSTRAINT orderitems_orderid_fkey FOREIGN KEY (orderid) REFERENCES public.orders(orderid);


--
-- Name: orderitems orderitems_productid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orderitems
    ADD CONSTRAINT orderitems_productid_fkey FOREIGN KEY (productid) REFERENCES public.inventory(productid);


--
-- Name: orders orders_customeremail_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customeremail_fkey FOREIGN KEY (customeremail) REFERENCES public.customeruser(customeremail);


--
-- Name: payment payment_orderid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_orderid_fkey FOREIGN KEY (orderid) REFERENCES public.orders(orderid);


--
-- Name: review review_customeremail_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_customeremail_fkey FOREIGN KEY (customeremail) REFERENCES public.customeruser(customeremail);


--
-- Name: review review_orderid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_orderid_fkey FOREIGN KEY (orderid) REFERENCES public.orders(orderid);


--
-- PostgreSQL database dump complete
--

