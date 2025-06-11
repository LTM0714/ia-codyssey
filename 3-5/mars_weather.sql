use mars_weather;

CREATE TABLE mars_weather(
	weatehr_id int AUTO_INCREMENT PRIMARY KEY,
    mars_date datetime NOT NULL,
    temp float,
    storm int
);

DROP TABLE mars_weather;

SELECT * FROM mars_weather;