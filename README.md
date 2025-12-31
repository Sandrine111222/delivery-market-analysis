# Description 📊




This project analyzes Delivery data to uncover actionable insights for restaurant partners and consumers. The objective is to explore trends, customer preferences, and market dynamics in the food delivery space, by conducting exploratory analysis, summarize findings, and present actionable insights.


---

# Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Dataset](#dataset)  
- [Building the SQL pipeline](#building-the-sql-pipeline)   
- [Creating visuals in PowerBI](#creating-visuals-in-powerbi)  
- [Project Structure](#project-structure)   


---

# Project Overview

The project includes:

- creating a pipeline using SQL queries
- creating csv files 
- building visuals in PowerBI

---

# Features

Enhance our data engineering and analytical skills by:
- Working with SQL operations like:
  - SELECT
  - JOIN
  - GROUP BY
  - Aggregations (e.g., average, sum)
  - Advanced queries
- Working with PowerBI
- Exploring geospatial data analysis
- Extracting and visualizing insights from food delivery datasets
- Building data storytelling and presentation skills 

---

# Dataset

The raw dataset is structured as a SQLite file.
The work refers to the database diagram. Usage of SQL queries allows explorating relationships between tables and derive insights.

  
  
---

# Building the SQL pipeline


## Key steps

1. **Cleaning of the data**  
   - Put everything in English only.
   - Correct spelling mistakes.
   - Group into smaller amount of subcategories per table.
   - Handle "zero" and "NULL". 

2. **Answer 10 questions**  
   - Key business questions:
      1. What is the price distribution of menu items?
      2. What is the distribution of restaurants per location?
      3. Which are the top 10 pizza restaurants by rating?
      4. Map locations offering kapsalons (or your favorite dish) and their average price.

   - Open ended questions:

      1. Which restaurants have the best price-to-rating ratio?
      2. Where are the delivery ‘dead zones’—areas with minimal restaurant coverage?
      3. How does the availability of vegetarian and vegan dishes vary by area?
      4. Identify the **World Hummus Order (WHO)**; top 3 hummus serving restaurants.
      5. What are the top 10 restaurants for deserts?
      6. What are the 10 worst restaurants?
    
  - SQL queries have been optimized for speed and readability.

3. **Store in CSV files**  
   - CSV files circumvent SQLite extension issues and PowerBI restrictions.

---

# Creating visuals in PowerBI


- Maps, tables, bar charts are made accordingly to the desired question.
  


---


# Project Structure

```bash
delivery-market-analysis/
│
├──cleaned_db.sql
├──ER_schema_takeaway.png
├──pipeline_sql.py
├──README.md
├──Top 10 pizzas.pbix
├──csv_exports
│    └──best_value_restaurants.csv
│    └──delivery_dead_zones.csv
│    └──kapsalon_map.csv
│    └──price_distribution.csv
│    └──restaurants_per_city.csv
│    └──top_10_pizza_restaurants.csv
│    └──veg_vegan_distribution.csv
│    └──world_hummus_order.csv
└── venv/  
     

---


This project is part of AI & Data Science Bootcamp training at **`</becode>`** and it written by :

- Sandrine Herbelet  [LinkedIn](https://www.linkedin.com/in/) | [Github](https://github.com/Sandrine111222)

