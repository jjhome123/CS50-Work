CREATE TABLE words (
    id INTEGER,
    word TEXT NOT NULL,
    usage TEXT NOT NULL,
    meaning TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE examples (
    id INTEGER,
    example TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES words(id),
    PRIMARY KEY(id)
);

-- Python command:
-- INSERT INTO words (word, usage, meaning) VALUES (?, ?, ?)