USE ev_db;

-- 0. Sanity checks
SELECT COUNT(*) AS total_rows FROM ev_market;
SELECT COUNT(DISTINCT manufacturer) AS manufacturers, COUNT(DISTINCT category) AS categories FROM ev_market;

-- 1. Top 10 manufacturers by total annual sales
SELECT manufacturer, SUM(annual_sales_units) AS total_sales
FROM ev_market GROUP BY manufacturer ORDER BY total_sales DESC LIMIT 10;

-- 2. Sales and average price by category
SELECT category, COUNT(*) AS models, SUM(annual_sales_units) AS total_sales,
       ROUND(AVG(price_usd),2) AS avg_price
FROM ev_market GROUP BY category ORDER BY total_sales DESC;

-- 3. Battery technology comparison
SELECT battery_type,
       ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(charging_dc_fast_time_min),1) AS avg_fast_charge_min,
       ROUND(AVG(battery_cycle_life),0) AS avg_cycle_life,
       ROUND(AVG(battery_degradation_pct_5yr),2) AS avg_degradation_pct
FROM ev_market GROUP BY battery_type ORDER BY avg_cycle_life DESC;

-- 4. Region-wise performance
SELECT market_region, COUNT(*) AS models, ROUND(AVG(price_usd),0) AS avg_price,
       ROUND(AVG(customer_rating),2) AS avg_rating,
       ROUND(SUM(co2_saved_tons_per_year),1) AS co2_saved_tons
FROM ev_market GROUP BY market_region ORDER BY models DESC;

-- 5. Year-wise trend
SELECT model_year, COUNT(*) AS models, ROUND(AVG(range_km),1) AS avg_range_km,
       ROUND(AVG(price_usd),0) AS avg_price
FROM ev_market GROUP BY model_year ORDER BY model_year;

-- 6. Best value vehicles (km of range per 1000 USD)
SELECT model_name, manufacturer, category, price_usd, range_km,
       ROUND(range_km / price_usd * 1000, 2) AS km_per_1000usd
FROM ev_market WHERE price_usd > 0
ORDER BY km_per_1000usd DESC LIMIT 20;

-- 7. Manufacturing country summary
SELECT manufacturing_country, COUNT(*) AS models, ROUND(AVG(safety_rating_stars),2) AS avg_safety
FROM ev_market GROUP BY manufacturing_country ORDER BY models DESC;

-- 8. Use-case summary
SELECT recommended_use_case, COUNT(*) AS models, ROUND(AVG(price_usd),0) AS avg_price
FROM ev_market GROUP BY recommended_use_case ORDER BY models DESC;

-- 9. Missing-value audit
SELECT SUM(resale_value_pct_3yr IS NULL) AS null_resale,
       SUM(battery_cycle_life IS NULL) AS null_cycle_life,
       SUM(customer_rating IS NULL) AS null_rating,
       SUM(infotainment_screen_inch IS NULL) AS null_screen,
       SUM(annual_sales_units IS NULL) AS null_sales
FROM ev_market;

-- 10. Clean view used by Tableau (derived fields included)
CREATE OR REPLACE VIEW vw_ev_clean AS
SELECT *,
       ROUND(range_km / price_usd * 1000, 2) AS range_per_1000usd,
       CASE WHEN price_usd < 20000 THEN 'Budget'
            WHEN price_usd < 60000 THEN 'Mid-range'
            WHEN price_usd < 120000 THEN 'Premium' ELSE 'Luxury' END AS price_segment,
       CASE WHEN range_km < 250 THEN 'Short'
            WHEN range_km < 450 THEN 'Medium' ELSE 'Long' END AS range_class,
       price_usd * annual_sales_units AS est_revenue_usd
FROM ev_market
WHERE price_usd > 0 AND range_km > 0;
