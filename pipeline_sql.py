import duckdb
import os


# CONFIG — Windows + Power BI Free safe


DB_PATH = r"C:/Users/sandy/Desktop/delivery-market-analysis/takeaway.db"
EXPORT_DIR = r"C:/Users/sandy/OneDrive/Documents/PowerBI_CSVs"

os.makedirs(EXPORT_DIR, exist_ok=True)


# CONNECT TO DUCKDB (IN-MEMORY)


con = duckdb.connect(database=":memory:")

con.execute("""
INSTALL sqlite;
LOAD sqlite;
""")

con.execute(f"""
ATTACH '{DB_PATH}' AS sqlite_db (TYPE SQLITE);
""")

# 1) CLEAN LOCATIONS


con.execute("""
CREATE TABLE cleaned_locations AS
SELECT
    id AS location_id,
    CASE
        WHEN TRY_CAST(postalCode AS VARCHAR) IN ('0','') THEN NULL
        ELSE TRIM(TRY_CAST(postalCode AS VARCHAR))
    END AS postal_code,
    CASE
        WHEN TRY_CAST(latitude AS DOUBLE) BETWEEN -90 AND 90 THEN TRY_CAST(latitude AS DOUBLE)
        ELSE NULL
    END AS latitude,
    CASE
        WHEN TRY_CAST(longitude AS DOUBLE) BETWEEN -180 AND 180 THEN TRY_CAST(longitude AS DOUBLE)
        ELSE NULL
    END AS longitude,
    CASE
        WHEN TRY_CAST(city AS VARCHAR) IN ('0','') THEN NULL
        ELSE LOWER(TRIM(TRY_CAST(city AS VARCHAR)))
    END AS city
FROM sqlite_db.locations;
""")


# 2) CLEAN RESTAURANTS


con.execute("""
CREATE TABLE cleaned_restaurants AS
SELECT
    LOWER(TRIM(TRY_CAST(primarySlug AS VARCHAR))) AS restaurant_key,
    CASE
        WHEN TRY_CAST(name AS VARCHAR) IN ('0','') THEN NULL
        ELSE TRIM(TRY_CAST(name AS VARCHAR))
    END AS restaurant_name,
    CASE
        WHEN TRY_CAST(city AS VARCHAR) IN ('0','') THEN NULL
        ELSE LOWER(TRIM(TRY_CAST(city AS VARCHAR)))
    END AS city,
    CASE
        WHEN LOWER(TRY_CAST(supportsDelivery AS VARCHAR)) IN ('true','1','yes','y') THEN 1
        WHEN LOWER(TRY_CAST(supportsDelivery AS VARCHAR)) IN ('false','0','no','n') THEN 0
        ELSE NULL
    END AS supports_delivery,
    CASE
        WHEN TRY_CAST(ratings AS DOUBLE) BETWEEN 0 AND 5 THEN TRY_CAST(ratings AS DOUBLE)
        ELSE NULL
    END AS rating,
    CASE
        WHEN TRY_CAST(ratingsNumber AS BIGINT) > 0 THEN TRY_CAST(ratingsNumber AS BIGINT)
        ELSE NULL
    END AS rating_count,
    CASE
        WHEN TRY_CAST(latitude AS DOUBLE) BETWEEN -90 AND 90 THEN TRY_CAST(latitude AS DOUBLE)
        ELSE NULL
    END AS latitude,
    CASE
        WHEN TRY_CAST(longitude AS DOUBLE) BETWEEN -180 AND 180 THEN TRY_CAST(longitude AS DOUBLE)
        ELSE NULL
    END AS longitude
FROM sqlite_db.restaurants;
""")

# 3) CLEAN MENU ITEMS


con.execute("""
CREATE TABLE cleaned_menu_items AS
SELECT
    LOWER(TRIM(TRY_CAST(primarySlug AS VARCHAR))) AS restaurant_key,
    id AS item_id,
    CASE
        WHEN TRY_CAST(name AS VARCHAR) IN ('0','') THEN NULL
        ELSE LOWER(TRIM(TRY_CAST(name AS VARCHAR)))
    END AS item_name,
    CASE
        WHEN TRY_CAST(price AS DOUBLE) > 0 THEN TRY_CAST(price AS DOUBLE)
        ELSE NULL
    END AS price
FROM sqlite_db.menuItems;
""")

# BUSINESS QUESTIONS


# PRICE DISTRIBUTION
con.execute("""
CREATE TABLE price_distribution AS
SELECT
    ROUND(price, 2) AS price,
    COUNT(*) AS item_count
FROM cleaned_menu_items
WHERE price IS NOT NULL
GROUP BY price
ORDER BY price;
""")

# RESTAURANTS PER CITY
con.execute("""
CREATE TABLE restaurants_per_city AS
SELECT
    city,
    COUNT(*) AS restaurant_count
FROM cleaned_restaurants
WHERE city IS NOT NULL
GROUP BY city
ORDER BY restaurant_count DESC;
""")

# TOP 10 PIZZA RESTAURANTS
con.execute("""
CREATE TABLE top_10_pizza_restaurants AS
SELECT
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count
FROM cleaned_restaurants r
JOIN cleaned_menu_items m
    ON r.restaurant_key = m.restaurant_key
WHERE m.item_name LIKE '%pizza%'
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count
ORDER BY r.rating DESC, r.rating_count DESC
LIMIT 10;
""")

# TOP 10 DESSERT RESTAURANTS
con.execute("""
CREATE TABLE top_10_dessert_restaurants AS
SELECT
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count,
    COUNT(*) AS dessert_items,
    ROUND(AVG(m.price), 2) AS avg_dessert_price
FROM cleaned_restaurants r
JOIN cleaned_menu_items m
    ON r.restaurant_key = m.restaurant_key
WHERE
    m.item_name LIKE '%dessert%'
    OR m.item_name LIKE '%cake%'
    OR m.item_name LIKE '%ice cream%'
    OR m.item_name LIKE '%brownie%'
    OR m.item_name LIKE '%tiramisu%'
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count
ORDER BY r.rating DESC, r.rating_count DESC
LIMIT 10;
""")

# KAPSALON MAP
con.execute("""
CREATE TABLE kapsalon_map AS
SELECT
    r.restaurant_name,
    r.city,
    r.latitude,
    r.longitude,
    COUNT(*) AS kapsalon_items,
    ROUND(AVG(m.price), 2) AS avg_price
FROM cleaned_menu_items m
JOIN cleaned_restaurants r
    ON m.restaurant_key = r.restaurant_key
WHERE m.item_name LIKE '%kapsalon%'
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city,
    r.latitude,
    r.longitude;
""")

# BEST PRICE-TO-RATING RATIO
con.execute("""
CREATE TABLE best_value_restaurants AS
SELECT
    r.restaurant_name,
    r.city,
    r.rating,
    ROUND(AVG(m.price), 2) AS avg_price,
    ROUND(AVG(m.price) / r.rating, 2) AS price_to_rating_ratio
FROM cleaned_restaurants r
JOIN cleaned_menu_items m
    ON r.restaurant_key = m.restaurant_key
WHERE r.rating IS NOT NULL AND r.rating >= 3
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city,
    r.rating
ORDER BY price_to_rating_ratio ASC
LIMIT 15;
""")

# WORST 10 RESTAURANTS
con.execute("""
CREATE TABLE worst_10_restaurants AS
SELECT
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count,
    ROUND(AVG(m.price), 2) AS avg_price,
    ROUND(AVG(m.price) / r.rating, 2) AS price_to_rating_ratio
FROM cleaned_restaurants r
JOIN cleaned_menu_items m
    ON r.restaurant_key = m.restaurant_key
WHERE r.rating IS NOT NULL
  AND r.rating <= 3.5
  AND m.price IS NOT NULL
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city,
    r.rating,
    r.rating_count
ORDER BY price_to_rating_ratio DESC
LIMIT 10;
""")

# DELIVERY DEAD ZONES
con.execute("""
CREATE TABLE delivery_dead_zones AS
SELECT
    city,
    COUNT(*) AS restaurant_count
FROM cleaned_restaurants
WHERE supports_delivery = 1
GROUP BY city
HAVING restaurant_count < 3
ORDER BY restaurant_count;
""")

# VEGAN / VEGETARIAN AVAILABILITY
con.execute("""
CREATE TABLE veg_vegan_distribution AS
SELECT
    r.city,
    COUNT(CASE WHEN m.item_name LIKE '%vegan%' THEN 1 END) AS vegan_items,
    COUNT(CASE WHEN m.item_name LIKE '%vegetarian%' OR m.item_name LIKE '%veggie%' THEN 1 END) AS vegetarian_items
FROM cleaned_menu_items m
JOIN cleaned_restaurants r
    ON m.restaurant_key = r.restaurant_key
GROUP BY r.city;
""")

# WORLD HUMMUS ORDER (WHO)
con.execute("""
CREATE TABLE world_hummus_order AS
SELECT
    r.restaurant_name,
    r.city,
    COUNT(*) AS hummus_items,
    ROUND(AVG(m.price), 2) AS avg_hummus_price
FROM cleaned_menu_items m
JOIN cleaned_restaurants r
    ON m.restaurant_key = r.restaurant_key
WHERE m.item_name LIKE '%hummus%'
GROUP BY
    r.restaurant_key,
    r.restaurant_name,
    r.city
ORDER BY hummus_items DESC, avg_hummus_price ASC
LIMIT 3;
""")

# EXPORT TO CSV (POWER BI FREE SAFE)


tables = [
    "price_distribution",
    "restaurants_per_city",
    "top_10_pizza_restaurants",
    "top_10_dessert_restaurants",
    "kapsalon_map",
    "best_value_restaurants",
    "worst_10_restaurants",
    "delivery_dead_zones",
    "veg_vegan_distribution",
    "world_hummus_order"
]

for table in tables:
    con.execute(f"""
        COPY (SELECT * FROM {table})
        TO '{EXPORT_DIR}/{table}.csv'
        (HEADER, DELIMITER ',');
    """)

print("PIPELINE COMPLETED — ALL CSVs READY FOR POWER BI")

