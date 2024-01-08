SELECT AVG(rating)
FROM ratings
WHERE movie_id In (SELECT id FROM movies WHERE year LIKE "2012")