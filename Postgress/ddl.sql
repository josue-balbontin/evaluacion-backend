-- ============================================================
-- DDL – Restaurant Reservations  (Option C)
-- Schema: content
-- All domain tables use UUID primary keys and
-- created / modified timestamp-with-timezone columns.
-- ============================================================

-- 0. Create the schema
CREATE SCHEMA IF NOT EXISTS content;

-- ============================================================
-- 1. Restaurant
-- ============================================================
CREATE TABLE content.restaurant (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255)    NOT NULL,
    slug            VARCHAR(255)    NOT NULL UNIQUE,
    description     TEXT            NOT NULL DEFAULT '',
    address         VARCHAR(500)    NOT NULL DEFAULT '',
    phone           VARCHAR(30)     NOT NULL DEFAULT '',
    email           VARCHAR(254)    NOT NULL DEFAULT '',
    website         VARCHAR(500)    NOT NULL DEFAULT '',
    opening_time    TIME            NOT NULL DEFAULT '08:00',
    closing_time    TIME            NOT NULL DEFAULT '23:00',
    timezone        VARCHAR(63)     NOT NULL DEFAULT 'UTC',
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_restaurant_slug      ON content.restaurant (slug);
CREATE INDEX idx_restaurant_is_active ON content.restaurant (is_active);

COMMENT ON TABLE content.restaurant IS 'A restaurant establishment managed through the admin panel.';

-- ============================================================
-- 2. TableType
-- ============================================================
CREATE TABLE content.table_type (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL
                        REFERENCES content.restaurant (id)
                        ON DELETE CASCADE,
    name            VARCHAR(120)    NOT NULL,
    description     TEXT            NOT NULL DEFAULT '',
    seats           INTEGER         NOT NULL CHECK (seats > 0),
    quantity        INTEGER         NOT NULL DEFAULT 1 CHECK (quantity > 0),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_table_type_restaurant ON content.table_type (restaurant_id);
CREATE INDEX idx_table_type_active     ON content.table_type (is_active);

COMMENT ON TABLE content.table_type IS
  'A category of tables within a restaurant (e.g. "Window 2-seater", "Terrace 6-seater").';
COMMENT ON COLUMN content.table_type.seats IS 'Number of seats per individual table of this type.';
COMMENT ON COLUMN content.table_type.quantity IS 'How many physical tables of this type exist in the restaurant.';

-- ============================================================
-- 3. MenuItem
-- ============================================================
CREATE TABLE content.menu_item (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL
                        REFERENCES content.restaurant (id)
                        ON DELETE CASCADE,
    name            VARCHAR(255)    NOT NULL,
    description     TEXT            NOT NULL DEFAULT '',
    course          VARCHAR(60)     NOT NULL DEFAULT 'Main',
    price           DECIMAL(10, 2)  NOT NULL CHECK (price >= 0),
    allergens       TEXT[]          NOT NULL DEFAULT '{}',
    is_available    BOOLEAN         NOT NULL DEFAULT TRUE,
    available_from  DATE            NULL,
    available_until DATE            NULL,
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now(),
    CONSTRAINT chk_menu_item_dates CHECK (
        available_from IS NULL
        OR available_until IS NULL
        OR available_from <= available_until
    )
);

CREATE INDEX idx_menu_item_restaurant  ON content.menu_item (restaurant_id);
CREATE INDEX idx_menu_item_available   ON content.menu_item (is_available);
CREATE INDEX idx_menu_item_course      ON content.menu_item (course);

COMMENT ON TABLE content.menu_item IS 'A dish or drink served by the restaurant.';
COMMENT ON COLUMN content.menu_item.allergens IS 'Array of allergen identifiers (e.g. {"gluten","dairy"}).';
COMMENT ON COLUMN content.menu_item.available_from IS 'First date the dish is offered (NULL = always).';
COMMENT ON COLUMN content.menu_item.available_until IS 'Last date the dish is offered (NULL = indefinitely).';

-- ============================================================
-- 4. PricingTier  (Business Logic – Pricing Rules)
-- ============================================================
CREATE TABLE content.pricing_tier (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    table_type_id   UUID            NOT NULL
                        REFERENCES content.table_type (id)
                        ON DELETE CASCADE,
    name            VARCHAR(120)    NOT NULL,
    price_per_seat  DECIMAL(10, 2)  NOT NULL CHECK (price_per_seat >= 0),
    priority        INTEGER         NOT NULL DEFAULT 0,
    valid_from      TIMESTAMPTZ     NULL,
    valid_until     TIMESTAMPTZ     NULL,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now(),
    CONSTRAINT chk_pricing_tier_dates CHECK (
        valid_from IS NULL
        OR valid_until IS NULL
        OR valid_from <= valid_until
    )
);

CREATE INDEX idx_pricing_tier_table_type ON content.pricing_tier (table_type_id);
CREATE INDEX idx_pricing_tier_active     ON content.pricing_tier (is_active);
CREATE INDEX idx_pricing_tier_validity   ON content.pricing_tier (valid_from, valid_until);

COMMENT ON TABLE content.pricing_tier IS
  'Time-bound pricing for a TableType. The tier with the highest priority '
  'that is currently valid wins. If priorities tie, the most recently created tier wins.';

-- ============================================================
-- 5. Reservation
-- ============================================================
CREATE TABLE content.reservation (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID            NOT NULL
                        REFERENCES content.restaurant (id)
                        ON DELETE CASCADE,
    table_type_id   UUID            NOT NULL
                        REFERENCES content.table_type (id)
                        ON DELETE CASCADE,
    reservation_date DATE           NOT NULL,
    reservation_time TIME           NOT NULL,
    party_size      INTEGER         NOT NULL CHECK (party_size > 0),
    customer_name   VARCHAR(255)    NOT NULL,
    customer_email  VARCHAR(254)    NOT NULL DEFAULT '',
    customer_phone  VARCHAR(30)     NOT NULL DEFAULT '',
    notes           TEXT            NOT NULL DEFAULT '',
    status          VARCHAR(20)     NOT NULL DEFAULT 'confirmed'
                        CHECK (status IN (
                            'pending', 'confirmed', 'seated',
                            'completed', 'cancelled', 'no_show'
                        )),
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_reservation_restaurant ON content.reservation (restaurant_id);
CREATE INDEX idx_reservation_table_type ON content.reservation (table_type_id);
CREATE INDEX idx_reservation_date       ON content.reservation (reservation_date);
CREATE INDEX idx_reservation_status     ON content.reservation (status);
CREATE INDEX idx_reservation_datetime   ON content.reservation (reservation_date, reservation_time);

COMMENT ON TABLE content.reservation IS
  'A booking for a specific table type at a restaurant on a given date/time.';

-- ============================================================
-- 6. ReservationGuest
-- ============================================================
CREATE TABLE content.reservation_guest (
    id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_id  UUID            NOT NULL
                        REFERENCES content.reservation (id)
                        ON DELETE CASCADE,
    full_name       VARCHAR(255)    NOT NULL,
    email           VARCHAR(254)    NOT NULL DEFAULT '',
    phone           VARCHAR(30)     NOT NULL DEFAULT '',
    dietary_notes   TEXT            NOT NULL DEFAULT '',
    is_primary      BOOLEAN         NOT NULL DEFAULT FALSE,
    created         TIMESTAMPTZ     NOT NULL DEFAULT now(),
    modified        TIMESTAMPTZ     NOT NULL DEFAULT now()
);

CREATE INDEX idx_reservation_guest_reservation ON content.reservation_guest (reservation_id);

COMMENT ON TABLE content.reservation_guest IS
  'An individual guest associated with a reservation.';

-- ============================================================
-- Trigger function: auto-update `modified` on UPDATE
-- ============================================================
CREATE OR REPLACE FUNCTION content.set_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to every domain table
CREATE TRIGGER trg_restaurant_modified
    BEFORE UPDATE ON content.restaurant
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();

CREATE TRIGGER trg_table_type_modified
    BEFORE UPDATE ON content.table_type
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();

CREATE TRIGGER trg_menu_item_modified
    BEFORE UPDATE ON content.menu_item
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();

CREATE TRIGGER trg_pricing_tier_modified
    BEFORE UPDATE ON content.pricing_tier
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();

CREATE TRIGGER trg_reservation_modified
    BEFORE UPDATE ON content.reservation
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();

CREATE TRIGGER trg_reservation_guest_modified
    BEFORE UPDATE ON content.reservation_guest
    FOR EACH ROW EXECUTE FUNCTION content.set_modified();
