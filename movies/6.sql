-- In 6.sql, write a SQL query to determine the average rating of all movies released in 2012.
-- Your query should output a table with a single column and a single row (not counting the header) containing the average rating.

SELECT AVG(rating)
FROM movies m
INNER JOIN ratings r ON m.id = r.movie_id
WHERE year = 2012;
