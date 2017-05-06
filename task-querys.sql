-- 1) Вывести	все	года,	где	были	фильмы,	оцененные	на	4,	5
SELECT DISTINCT year FROM movie JOIN rating USING (mID) WHERE stars=4 OR stars=5;
-- 2) Вывести	всех	обзорщиков,	которые	не	поставили	даты
SELECT name AS reviewer_name FROM reviewer JOIN rating USING (rID) WHERE ratingDate IS NULL;
-- 3) Вывести	максимальный	рейтинг фильма
SELECT title, MAX(stars) AS max_rating FROM movie JOIN rating USING (mID) GROUP BY mID;
-- 4) Вывести	неоцененные	фильмы
SELECT title FROM movie LEFT JOIN rating USING (mID) WHERE stars IS NULL;
-- 5) Вывести	обзорщиков на фильм GONE	WITH	THE	WIND
SELECT DISTINCT name AS reviewer_name FROM reviewer JOIN rating USING (rID) JOIN movie USING (mID) WHERE title="Gone with the Wind";
-- 6) Вывести	разницу	между	мин. и	макс.	рейтингом	фильма
SELECT title, MAX(stars)-MIN(stars) AS max_rating_diff FROM rating JOIN movie USING (mID) GROUP BY mID;
