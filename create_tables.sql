CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    month VARCHAR(20),
    subject_matter VARCHAR(100)
);

CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    episode_id INTEGER NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id)
);
