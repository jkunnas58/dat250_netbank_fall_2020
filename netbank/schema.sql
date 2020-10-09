DROP TABLE IF EXISTS article;

CREATE TABLE article
(
    id INTEGER PRIMARY KEY,
    title TEXT,
    text TEXT,
    date TEXT
);

INSERT INTO article
    (title, text, date)
VALUES('Something bad happened today', 'Today was a bad day', '1999-04-12'),
    ('Something good happened today', 'Today was a good day', '2004-04-01');