-- 1. Movies Only

CREATE VIEW IF NOT EXISTS movie_catalog AS

SELECT *

FROM netflix_titles

WHERE type = 'Movie';

-------------------------------------------------------------
-- 2. TV Shows Only
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS tv_catalog AS

SELECT *

FROM netflix_titles

WHERE type = 'TV Show';

-------------------------------------------------------------
-- 3. Recently Released Content
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS recent_content AS

SELECT *

FROM netflix_titles

WHERE release_year >= 2020;

-------------------------------------------------------------
-- 4. Classic Content
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS classic_content AS

SELECT *

FROM netflix_titles

WHERE release_year < 2000;

-------------------------------------------------------------
-- 5. Long Movies
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS long_movies AS

SELECT *

FROM netflix_titles

WHERE type='Movie'

AND duration_minutes >= 120;

-------------------------------------------------------------
-- 6. Short Movies
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS short_movies AS

SELECT *

FROM netflix_titles

WHERE type='Movie'

AND duration_minutes < 90;

-------------------------------------------------------------
-- 7. Family Friendly
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS family_content AS

SELECT *

FROM netflix_titles

WHERE rating IN (

'G',
'PG',
'TV-G',
'TV-PG',
'TV-Y',
'TV-Y7'

);

-------------------------------------------------------------
-- 8. Mature Content
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS mature_content AS

SELECT *

FROM netflix_titles

WHERE rating IN (

'R',
'TV-MA',
'NC-17'

);

-------------------------------------------------------------
-- 9. Highly Diverse Titles
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS diverse_titles AS

SELECT *

FROM netflix_titles

WHERE genre_count >= 3

AND country_count >= 2;

-------------------------------------------------------------
-- 10. Recommendation Candidates
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS recommendation_candidates AS

SELECT

title,

type,

release_year,

listed_in,

country,

duration_category,

popularity_score

FROM netflix_titles

ORDER BY popularity_score DESC;

-------------------------------------------------------------
-- 11. Yearly Production
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS yearly_production AS

SELECT

release_year,

COUNT(*) AS total_titles

FROM netflix_titles

GROUP BY release_year;

-------------------------------------------------------------
-- 12. Rating Distribution
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS rating_distribution AS

SELECT

rating,

COUNT(*) AS total_titles

FROM netflix_titles

GROUP BY rating;

-------------------------------------------------------------
-- 13. Duration Statistics
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS duration_statistics AS

SELECT

duration_category,

COUNT(*) AS total_titles,

AVG(duration_minutes) AS avg_duration

FROM netflix_titles

WHERE type='Movie'

GROUP BY duration_category;

-------------------------------------------------------------
-- 14. Content Added Per Year
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS yearly_additions AS

SELECT

year_added,

COUNT(*) AS titles_added

FROM netflix_titles

GROUP BY year_added;

-------------------------------------------------------------
-- 15. Business KPI View
-------------------------------------------------------------

CREATE VIEW IF NOT EXISTS executive_summary AS

SELECT

COUNT(*) AS total_titles,

SUM(CASE WHEN type='Movie' THEN 1 ELSE 0 END) AS total_movies,

SUM(CASE WHEN type='TV Show' THEN 1 ELSE 0 END) AS total_tvshows,

AVG(content_age) AS average_content_age,

AVG(popularity_score) AS average_popularity

FROM netflix_titles;