-- BASIC DATASET INFORMATION
-- 1
SELECT COUNT(*) AS total_titles
FROM netflix_titles;

-- 2
SELECT type, COUNT(*) AS total
FROM netflix_titles
GROUP BY type;

-- RELEASE ANALYSIS

-- 3
SELECT release_year, COUNT(*) AS titles
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year;

-- 4
SELECT year_added, COUNT(*) AS added
FROM netflix_titles
GROUP BY year_added
ORDER BY year_added;

-- ==========================================
-- RATINGS
-- ==========================================

-- 5
SELECT rating, COUNT(*) AS total
FROM netflix_titles
GROUP BY rating
ORDER BY total DESC;

-- ==========================================
-- MOVIE DURATIONS
-- ==========================================

-- 6
SELECT
AVG(duration_minutes) AS average_runtime
FROM netflix_titles
WHERE type='Movie';

-- ==========================================
-- TV SHOWS
-- ==========================================

-- 7
SELECT
AVG(season_count) AS average_seasons
FROM netflix_titles
WHERE type='TV Show';

-- ==========================================
-- LONGEST MOVIES
-- ==========================================

-- 8
SELECT
title,
duration_minutes
FROM netflix_titles
WHERE type='Movie'
ORDER BY duration_minutes DESC
LIMIT 10;

-- ==========================================
-- LONGEST TV SHOWS
-- ==========================================

-- 9
SELECT
title,
season_count
FROM netflix_titles
WHERE type='TV Show'
ORDER BY season_count DESC
LIMIT 10;

-- ==========================================
-- CONTENT AGE
-- ==========================================

-- 10
SELECT
AVG(content_age)
FROM netflix_titles;

-- ==========================================
-- DURATION CATEGORY
-- ==========================================

-- 11
SELECT
duration_category,
COUNT(*)
FROM netflix_titles
GROUP BY duration_category;

-- ==========================================
-- POPULARITY SCORE
-- ==========================================

-- 12
SELECT
title,
popularity_score
FROM netflix_titles
ORDER BY popularity_score DESC
LIMIT 15;

-- ==========================================
-- OLDEST CONTENT
-- ==========================================

-- 13
SELECT
title,
release_year
FROM netflix_titles
ORDER BY release_year
LIMIT 15;

-- ==========================================
-- NEWEST CONTENT
-- ==========================================

-- 14
SELECT
title,
release_year
FROM netflix_titles
ORDER BY release_year DESC
LIMIT 15;

-- ==========================================
-- YEARS ON NETFLIX
-- ==========================================

-- 15
SELECT
AVG(years_on_netflix)
FROM netflix_titles;

-- ==========================================
-- MULTI COUNTRY TITLES
-- ==========================================

-- 16
SELECT
title,
country_count
FROM netflix_titles
ORDER BY country_count DESC
LIMIT 10;

-- ==========================================
-- MULTI GENRE TITLES
-- ==========================================

-- 17
SELECT
title,
genre_count
FROM netflix_titles
ORDER BY genre_count DESC
LIMIT 10;

-- ==========================================
-- LARGE CASTS
-- ==========================================

-- 18
SELECT
title,
cast_count
FROM netflix_titles
ORDER BY cast_count DESC
LIMIT 10;

-- ==========================================
-- MOST RECENTLY ADDED
-- ==========================================

-- 19
SELECT
title,
date_added
FROM netflix_titles
ORDER BY date(date_added) DESC
LIMIT 15;

-- ==========================================
-- OLDEST ADDED
-- ==========================================

-- 20
SELECT
title,
date_added
FROM netflix_titles
ORDER BY date(date_added)
LIMIT 15;