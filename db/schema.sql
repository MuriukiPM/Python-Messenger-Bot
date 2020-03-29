CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    messenger_id VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT NOW(),
    age INTEGER DEFAULT 0,
    gender VARCHAR(255) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    is_complete INTEGER,
    created_at timestamp DEFAULT current_timestamp,
    updated_at timestamp DEFAULT NOW()
);