-- ADVANCED SQL QUERIES
-- 1. ROW_NUMBER()

SELECT
    title,
    release_year,
    ROW_NUMBER() OVER(
        ORDER BY release_year DESC
    ) AS row_num
FROM netflix_titles;

-- 2.RANK()

SELECT
    title,
    release_year,
    RANK() OVER(
        ORDER BY release_year DESC
    ) AS ranking
FROM netflix_titles;

-- 3. DENSE_RANK()

SELECT
    title,
    release_year,
    DENSE_RANK() OVER(
        ORDER BY release_year DESC
    ) AS dense_rank
FROM netflix_titles;

-- 4. LAG()

SELECT
    release_year,
    COUNT(*) AS titles,
    LAG(COUNT(*),1)
    OVER(
        ORDER BY release_year
    ) AS previous_year
FROM netflix_titles
GROUP BY release_year;

--------------------------------------------------------------
-- 5. LEAD()
--------------------------------------------------------------

SELECT
    release_year,
    COUNT(*) AS titles,
    LEAD(COUNT(*),1)
    OVER(
        ORDER BY release_year
    ) AS next_year
FROM netflix_titles
GROUP BY release_year;

--------------------------------------------------------------
-- 6. CTE
--------------------------------------------------------------

WITH yearly_content AS (

SELECT
    release_year,
    COUNT(*) AS total_titles

FROM netflix_titles

GROUP BY release_year

)

SELECT *

FROM yearly_content

ORDER BY total_titles DESC;

--------------------------------------------------------------
-- 7. Recent Content
--------------------------------------------------------------

WITH recent AS (

SELECT *

FROM netflix_titles

WHERE release_year >= 2020

)

SELECT
type,
COUNT(*) AS total

FROM recent

GROUP BY type;

--------------------------------------------------------------
-- 8. CASE Statement
--------------------------------------------------------------

SELECT

title,

CASE

WHEN release_year >= 2020 THEN 'Recent'

WHEN release_year >= 2010 THEN 'Modern'

WHEN release_year >= 2000 THEN 'Classic'

ELSE 'Old'

END AS content_generation

FROM netflix_titles;

--------------------------------------------------------------
-- 9. Average Runtime by Category
--------------------------------------------------------------

SELECT

duration_category,

AVG(duration_minutes)

FROM netflix_titles

WHERE type='Movie'

GROUP BY duration_category;

--------------------------------------------------------------
-- 10. Top Years
--------------------------------------------------------------

SELECT

release_year,

COUNT(*) AS titles

FROM netflix_titles

GROUP BY release_year

HAVING COUNT(*) > 100

ORDER BY titles DESC;

--------------------------------------------------------------
-- 11. Ranking by Popularity Score
--------------------------------------------------------------

SELECT

title,

popularity_score,

RANK() OVER(

ORDER BY popularity_score DESC

) AS popularity_rank

FROM netflix_titles;

--------------------------------------------------------------
-- 12. Window Average
--------------------------------------------------------------

SELECT

title,

release_year,

AVG(content_age)

OVER()

AS average_content_age

FROM netflix_titles;

--------------------------------------------------------------
-- 13. Cumulative Titles
--------------------------------------------------------------

SELECT

release_year,

COUNT(*) AS yearly_titles,

SUM(COUNT(*))

OVER(

ORDER BY release_year

)

AS cumulative_titles

FROM netflix_titles

GROUP BY release_year;

--------------------------------------------------------------
-- 14. Longest Movies
--------------------------------------------------------------

WITH longest_movies AS (

SELECT

title,

duration_minutes

FROM netflix_titles

WHERE type='Movie'

)

SELECT *

FROM longest_movies

ORDER BY duration_minutes DESC

LIMIT 20;

--------------------------------------------------------------
-- 15. Multi-Genre Ranking
--------------------------------------------------------------

SELECT

title,

genre_count,

DENSE_RANK()

OVER(

ORDER BY genre_count DESC

)

AS genre_rank

FROM netflix_titles;