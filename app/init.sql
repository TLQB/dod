CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    last_login TIMESTAMP,
    created TIMESTAMP,
    modified TIMESTAMP,
    email VARCHAR(255),
    password VARCHAR(255),
    name VARCHAR(50) UNIQUE,
    is_mailauth_completed BOOLEAN,
    is_master BOOLEAN,
    is_enabled BOOLEAN,
    config JSONB,
    is_super BOOLEAN
);

INSERT INTO admins (email, password, name, is_mailauth_completed, is_master, is_enabled, config, is_super)
VALUES ('tranlequybaotk12@gmail.com', 'pbkdf2_sha256$260000$ew6hVtSRdUXukBLmVz79Xk$EGbPYYmgyz5KsauAb0ukAZyNSKDYtX3MXPVrCFJbJP8=', 'master', true, true, true, '{}', true);


CREATE TABLE mail_temps (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    hash VARCHAR(255) NOT NULL,
    expire_time TIMESTAMP NOT NULL,
    created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
