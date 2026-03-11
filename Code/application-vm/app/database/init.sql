CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES
('filip', 'password-for-show'),
('jonatan', 'password-for-show')
ON CONFLICT (username) DO NOTHING;

