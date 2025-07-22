-- Drop tables if they already exist (in reverse dependency order)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TEXT,
    updated_at TEXT
);

-- Create places table
CREATE TABLE places (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    owner_id TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY (owner_id) REFERENCES users (id)
);

-- Create reviews table
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    place_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT,
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create amenities table
CREATE TABLE amenities (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT,
    updated_at TEXT
);

-- Create many-to-many relation table between places and amenities
CREATE TABLE place_amenity (
    place_id TEXT NOT NULL,
    amenity_id TEXT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (amenity_id) REFERENCES amenities (id)
);

-- Insert initial admin user
INSERT INTO users (
    id, first_name, last_name, email, password, is_admin, created_at, updated_at
) VALUES (
    'admin-uuid-001',
    'Admin',
    'User',
    'admin@example.com',
    '$2b$12$P2RBwXfAnT6HnVX.C04z.ePO2.qWnDIX89/kMDDaosB3yn1I7eCZy', -- hash for "admin123"
    TRUE,
    datetime('now'),
    datetime('now')
);

-- Insert some amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('amenity-uuid-001', 'Wi-Fi', datetime('now'), datetime('now')),
('amenity-uuid-002', 'Air Conditioning', datetime('now'), datetime('now')),
('amenity-uuid-003', 'Kitchen', datetime('now'), datetime('now'));
