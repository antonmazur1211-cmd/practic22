-- Ініціалізаційний скрипт PostgreSQL
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка тестових даних
INSERT INTO users (name, email) VALUES 
    ('Anton Mazur', 'anton@example.com'),
    ('Test User', 'test@example.com')
ON CONFLICT (email) DO NOTHING;

-- Створення індексу для швидкого пошуку
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
