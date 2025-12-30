
-- FULL PIPELINE SCRIPT
-- Cleaning + Business Analytics
-- Database: takeaway.db (SQLite)


PRAGMA foreign_keys = OFF;


-- CLEAN LOCATIONS

DROP TABLE IF EXISTS cleaned_locations;
CREATE TABLE cleaned_locations AS
SELECT
    ID,
    CASE WHEN postalCode IN (0,'0','') THEN NULL ELSE postalCode END AS postalCode,
    CASE WHEN latitude BETWEEN -90 AND 90 THEN latitude ELSE NULL END AS latitude,
    CASE WHEN longitude BETWEEN -180 AND 180 THEN longitude ELSE NULL END AS longitude,
    CASE WHEN city IN (0,'0','') THEN NULL ELSE LOWER(TRIM(city)) END AS city,
    CASE WHEN name IN (0,'0','') THEN NULL ELSE TRIM(name) END AS name
FROM locations;

-- CLEAN RESTAURANTS

DROP TABLE IF EXISTS cleaned_restaurants;
CREATE TABLE cleaned_restaurants AS
SELECT
    primarySlug,
    CASE WHEN restaurant_id IN (0,'0','') THEN NULL ELSE TRIM(restaurant_id) END AS restaurant_id,
    CASE WHEN name IN (0,'0','') THEN NULL ELSE TRIM(name) END AS name,
    CASE WHEN address IN (0,'0','') THEN NULL ELSE TRIM(address) END AS address,
    CASE WHEN city IN (0,'0','') THEN NULL ELSE LOWER(TRIM(city)) END AS city,

    CASE
        WHEN LOWER(supportsDelivery) IN ('true','1','yes','y') THEN 1
        WHEN LOWER(supportsDelivery) IN ('false','0','no','n') THEN 0
        ELSE NULL
    END AS supportsDelivery,

    CASE
        WHEN LOWER(supportsPickup) IN ('true','1','yes','y') THEN 1
        WHEN LOWER(supportsPickup) IN ('false','0','no','n') THEN 0
        ELSE NULL
    END AS supportsPickup,

    CASE WHEN paymentMethods IN (0,'0','') THEN NULL ELSE TRIM(paymentMethods) END AS paymentMethods,

    CASE WHEN ratings BETWEEN 0 AND 5 THEN ratings ELSE NULL END AS ratings,
    CASE WHEN ratingsNumber > 0 THEN ratingsNumber ELSE NULL END AS ratingsNumber,

    CASE WHEN durationRangeMin > 0 THEN durationRangeMin ELSE NULL END AS durationRangeMin,
    CASE WHEN durationRangeMax > 0 THEN durationRangeMax ELSE NULL END AS durationRangeMax,

    CASE WHEN deliveryFee > 0 THEN deliveryFee ELSE NULL END AS deliveryFee,
    CASE WHEN minOrder > 0 THEN minOrder ELSE NULL END AS minOrder,

    CASE WHEN latitude BETWEEN -90 AND 90 THEN latitude ELSE NULL END AS latitude,
    CASE WHEN longitude BETWEEN -180 AND 180 THEN longitude ELSE NULL END AS longitude
FROM restaurants;


-- CLEAN MENU ITEMS

DROP TABLE IF EXISTS cleaned_menuItems;
CREATE TABLE cleaned_menuItems AS
SELECT
    primarySlug,
    id,
    CASE WHEN name IN (0,'0','') THEN NULL ELSE TRIM(name) END AS name,
    CASE WHEN description IN (0,'0','') THEN NULL ELSE TRIM(description) END AS description,
    CASE WHEN price > 0 THEN price ELSE NULL END AS price,
    CASE WHEN alcoholContent > 0 THEN alcoholContent ELSE NULL END AS alcoholContent,
    CASE WHEN caffeineContent > 0 THEN caffeineContent ELSE NULL END AS caffeineContent
FROM menuItems;


-- CLEAN CATEGORIES

DROP TABLE IF EXISTS cleaned_categories;
CREATE TABLE cleaned_categories AS
SELECT
    id,
    CASE WHEN restaurant_id IN (0,'0','') THEN NULL ELSE TRIM(restaurant_id) END AS restaurant_id,
    CASE WHEN name IN (0,'0','') THEN NULL ELSE TRIM(name) END AS name,
    CASE WHEN item_id IN (0,'0','') THEN NULL ELSE TRIM(item_id) END AS item_id
FROM categories;


-- PRICE DISTRIBUTION

DROP TABLE IF EXISTS price_distribution;
CREATE TABLE price_distribution AS
SELECT
    ROUND(price, 2) AS price,
    COUNT(*) AS item_count
FROM cleaned_menuItems
WHERE price IS NOT NULL
GROUP BY ROUND(price, 2);

-- RESTAURANTS PER CITY

DROP TABLE IF EXISTS restaurants_per_city;
CREATE TABLE restaurants_per_city AS
SELECT
    city,
    COUNT(DISTINCT primarySlug) AS restaurant_count
FROM cleaned_restaurants
WHERE city IS NOT NULL
GROUP BY city;


-- TOP 10 PIZZA RESTAURANTS

DROP TABLE IF EXISTS top_10_pizza_restaurants;
CREATE TABLE top_10_pizza_restaurants AS
SELECT
    r.name,
    r.city,
    r.ratings,
    r.ratingsNumber
FROM cleaned_restaurants r
JOIN cleaned_menuItems m
    ON r.primarySlug = m.primarySlug
WHERE LOWER(m.name) LIKE '%pizza%'
GROUP BY r.primarySlug
ORDER BY r.ratings DESC, r.ratingsNumber DESC
LIMIT 10;

-- BEST DESSERTS BY RATING

DROP TABLE IF EXISTS best_desserts;
CREATE TABLE best_desserts AS
SELECT
    r.name,
    r.city,
    r.ratings,
    COUNT(*) AS dessert_items,
    ROUND(AVG(m.price), 2) AS avg_price
FROM cleaned_menuItems m
JOIN cleaned_restaurants r
    ON m.primarySlug = r.primarySlug
WHERE LOWER(m.name) LIKE '%dessert%'
   OR LOWER(m.name) LIKE '%cake%'
   OR LOWER(m.name) LIKE '%ice cream%'
   OR LOWER(m.name) LIKE '%brownie%'
GROUP BY r.primarySlug
ORDER BY r.ratings DESC
LIMIT 10;


-- WORST VALUE RESTAURANTS

DROP TABLE IF EXISTS worst_value_restaurants;
CREATE TABLE worst_value_restaurants AS
SELECT
    r.name,
    r.city,
    r.ratings,
    ROUND(AVG(m.price), 2) AS avg_price,
    CASE WHEN r.ratings IS NOT NULL AND r.ratings != 0 
         THEN ROUND(AVG(m.price) / r.ratings, 2) 
         ELSE NULL 
    END AS price_to_rating_ratio
FROM cleaned_restaurants r
JOIN cleaned_menuItems m
    ON r.primarySlug = m.primarySlug
WHERE r.ratings <= 3.5
GROUP BY r.primarySlug
ORDER BY price_to_rating_ratio DESC
LIMIT 10;

-- EXPORT ALL TO CSV (for SQLite CLI)

.headers on
.mode csv

.output price_distribution.csv
SELECT * FROM price_distribution;

.output restaurants_per_city.csv
SELECT * FROM restaurants_per_city;

.output top_10_pizza_restaurants.csv
SELECT * FROM top_10_pizza_restaurants;

.output best_desserts.csv
SELECT * FROM best_desserts;

.output worst_value_restaurants.csv
SELECT * FROM worst_value_restaurants;

.output stdout





