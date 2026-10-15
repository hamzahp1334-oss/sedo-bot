-- SEDO MARTIAL ART Database Schema

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language TEXT DEFAULT 'am',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS advertisement_requests (
    id TEXT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    category TEXT,
    format TEXT,
    full_name TEXT,
    company_name TEXT,
    company_address TEXT,
    environment TEXT,
    username TEXT,
    phone TEXT,
    description TEXT,
    preferred_date TEXT,
    budget TEXT,
    file_path TEXT,
    notes TEXT,
    status TEXT DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS partnership_requests (
    id TEXT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    full_name TEXT,
    company_name TEXT,
    position TEXT,
    username TEXT,
    phone TEXT,
    offer_description TEXT,
    collab_type TEXT,
    message TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id TEXT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name TEXT,
    message TEXT,
    status TEXT DEFAULT 'unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT,
    event TEXT,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
