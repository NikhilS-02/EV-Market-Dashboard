# Tableau build guide

## 1. Connect
Tableau Desktop > Connect > MySQL > server/port/user/password > database `ev_db` > drag `vw_ev_clean`.
Choose **Extract** for the final workbook (faster), and test **Live** once for the performance table.

## 2. Calculated fields (6)
```
Range per $1000     = [range_km] / [price_usd] * 1000
Price Segment       = IF [price_usd] < 20000 THEN "Budget"
                      ELSEIF [price_usd] < 60000 THEN "Mid-range"
                      ELSEIF [price_usd] < 120000 THEN "Premium" ELSE "Luxury" END
Range Class         = IF [range_km] >= 450 THEN "Long" ELSEIF [range_km] >= 250 THEN "Medium" ELSE "Short" END
Fast Charge Rating  = IF [charging_dc_fast_time_min] <= 15 THEN "Ultra-fast"
                      ELSEIF [charging_dc_fast_time_min] <= 25 THEN "Fast" ELSE "Standard" END
Revenue (Est.)      = [price_usd] * [annual_sales_units]
Sales Share %       = SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))
```
If you use the view `vw_ev_clean`, some of these already exist as columns; recreate them in Tableau anyway so they count as calculated fields.

Also create a **Top N Manufacturers** parameter (integer, 5 to 30) and a calculated field
`Is Top N = RANK(SUM([annual_sales_units])) <= [Top N]` to filter the manufacturer chart.

## 3. Worksheets (12)
1. Sales by category (bar)
2. Sales by model year (line)
3. Top N manufacturers (bar)
4. Manufacturing country (filled map)
5. Region vs average price (bar)
6. Battery type share (donut)
7. Battery type: cycle life and degradation (dual axis / bar)
8. Price vs range by category (scatter)
9. Category x drivetrain (heat map)
10. Recommended use case (treemap)
11. CO2 saved by category and region (stacked bar)
12. Customer rating distribution (histogram)

## 4. Filters (6)
model_year, market_region, category, battery_type, Price Segment, Top N Manufacturers.
Right click each > Apply to Worksheets > All Using This Data Source.

## 5. Dashboards (3)
- Market Overview: KPI cards + sheets 1, 2, 3, 5
- Technology: sheets 6, 7, 8, 9
- Geography and Impact: sheets 4, 10, 11, 12
Set Size = Automatic. Create Phone and Tablet layouts via Device Preview.

## 6. Story (6 scenes)
1 Market snapshot, 2 Who sells most, 3 Price vs range, 4 Battery technology, 5 Regions and countries, 6 Recommendations.
Write a caption for each scene that states the finding.

## 7. Publish
Server > Tableau Public > Save to Tableau Public. Click Share > copy the view URL
(like https://public.tableau.com/views/Workbook/Dashboard) into `.env`.
