-- In 10.sql, write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.
-- Your query should output a table with a single column for the name of each person.
-- If a person directed more than one movie that received a rating of at least 9.0, they should only appear in your results once.

SELECT DISTINCT(p.name)
FROM directors d
INNER JOIN people p ON d.person_id = p.id
INNER JOIN movies m ON d.movie_id = m.id
INNER JOIN ratings r ON m.id = r.movie_id
WHERE r.rating >= 9.0;
