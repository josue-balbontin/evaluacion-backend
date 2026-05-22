-- DDL – Restaurant Reservations (Option C)
-- Schema: content | UUID PKs | Django-compatible

CREATE SCHEMA IF NOT EXISTS content;

-- 1. Restaurant
CREATE TABLE content.restaurant (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255)    NOT NULL,
    slug            VARCHAR(255)    NOT NULL UNIQUE,
    description     TEXT            DEFAULT '',
    address         VARCHAR(500)    DEFAULT '',
    phone           VARCHAR(30)     DEFAULT '',
    opening_time    TIME            DEFAULT '08:00',
    closing_time    TIME            DEFAULT '23:00',
    timezone        VARCHAR(63)     DEFAULT 'UTC',
    is_active       BOOLEAN         DEFAULT TRUE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);


CREATE TABLE content.table_type (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL REFERENCES content.restaurant(id) ON DELETE CASCADE,
    name            VARCHAR(120)    NOT NULL,
    description     TEXT            DEFAULT '',
    seats           INTEGER         NOT NULL,
    quantity        INTEGER         DEFAULT 1,
    price_per_seat  DECIMAL(10,2)   DEFAULT 0,
    is_active       BOOLEAN         DEFAULT TRUE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);


CREATE TABLE content.pricing_tier (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    table_type_id   UUID            NOT NULL REFERENCES content.table_type(id) ON DELETE CASCADE,
    name            VARCHAR(120)    NOT NULL,
    price_per_seat  DECIMAL(10,2)   NOT NULL,
    priority        INTEGER         DEFAULT 0,
    valid_from      TIMESTAMPTZ,
    valid_until     TIMESTAMPTZ,
    is_active       BOOLEAN         DEFAULT TRUE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);


CREATE TABLE content.menu_item (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL REFERENCES content.restaurant(id) ON DELETE CASCADE,
    name            VARCHAR(255)    NOT NULL,
    description     TEXT            DEFAULT '',
    course          VARCHAR(60)     DEFAULT 'Main',
    price           DECIMAL(10,2)   NOT NULL,
    allergens       TEXT[]          DEFAULT '{}',
    is_available    BOOLEAN         DEFAULT TRUE,
    available_from  DATE,
    available_until DATE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);


CREATE TABLE content.reservation_status (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(20)     NOT NULL UNIQUE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);

INSERT INTO content.reservation_status (name) VALUES
    ('pending'),
    ('confirmed'),
    ('seated'),
    ('completed'),
    ('cancelled'),
    ('no_show');


CREATE TABLE content.reservation (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL REFERENCES content.restaurant(id) ON DELETE CASCADE,
    table_type_id   UUID            NOT NULL REFERENCES content.table_type(id) ON DELETE CASCADE,
    status_id       UUID            NOT NULL REFERENCES content.reservation_status(id),
    reservation_date DATE           NOT NULL,
    reservation_time TIME           NOT NULL,
    party_size      INTEGER         NOT NULL,
    customer_name   VARCHAR(255)    NOT NULL,
    customer_email  VARCHAR(254)    DEFAULT '',
    customer_phone  VARCHAR(30)     DEFAULT '',
    notes           TEXT            DEFAULT '',
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);


CREATE TABLE content.reservation_guest (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id  UUID            NOT NULL REFERENCES content.reservation(id) ON DELETE CASCADE,
    full_name       VARCHAR(255)    NOT NULL,
    email           VARCHAR(254)    DEFAULT '',
    phone           VARCHAR(30)     DEFAULT '',
    dietary_notes   TEXT            DEFAULT '',
    is_primary      BOOLEAN         DEFAULT FALSE,
    created         TIMESTAMPTZ     DEFAULT now(),
    modified        TIMESTAMPTZ     DEFAULT now()
);
