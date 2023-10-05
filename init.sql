CREATE TABLE publications (
    publication_id SERIAL PRIMARY KEY,
    publication_title TEXT NOT NULL,
    publication_text TEXT NOT NULL,
    publication_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_is_published ON publications(is_published);
