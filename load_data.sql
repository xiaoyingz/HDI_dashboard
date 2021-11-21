SET GLOBAL local_infile=1;

CREATE DATABASE IF NOT EXISTS mp;

USE mp;

DROP TABLE IF EXISTS movie;

CREATE TABLE movie(
    imdb_title_id VARCHAR(20) NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    date_published VARCHAR(20) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    country VARCHAR(255) NOT NULL,
    language VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    writer VARCHAR(255) NOT NULL,
    production_company VARCHAR(255) NOT NULL,
    actors TEXT NOT NULL,
    description TEXT NOT NULL,
    avg_vote FLOAT NOT NULL,
    votes INT NOT NULL,
    budget VARCHAR(255) NOT NULL,
    usa_gross_income VARCHAR(255) NOT NULL,
    worldwide_gross_income VARCHAR(255) NOT NULL,
    metascore INT NOT NULL,
    reviews_from_users INT NOT NULL,
    reviews_from_critics INT NOT NULL
);

LOAD DATA LOCAL INFILE 'movie.csv' INTO TABLE movie FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES;
