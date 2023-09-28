CREATE TABLE publications (
    id SERIAL PRIMARY KEY,
    unix_timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_is_published ON publications(is_published);
