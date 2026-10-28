"""EV Market SQL demo: loads the CSV into a database (SQLite) and runs the project queries.
Take a screenshot of each result. Press Enter to go to the next query."""
import sqlite3, sys
from pathlib import Path
import pandas as pd

pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)

def find_csv():
    here = Path(__file__).resolve().parent
    spots = [here, here / "data" / "raw", Path.home() / "Downloads", Path.home() / "Desktop", Path.home() / "Documents"]
    for s in spots:
        p = s / "ev_market_test.csv"
        if p.exists(): return p
    for s in spots:                      # also look one level inside those folders
        if s.exists():
            hits = list(s.glob("*/ev_market_test.csv"))
            if hits: return hits[0]
    return None

csv = find_csv()
if csv is None:
    print("Could not find ev_market_test.csv.")
    print("Copy ev_market_test.csv into the same folder as sql_demo.py and run again.")
    input("Press Enter to close..."); sys.exit(1)

print(f"Found dataset: {csv}")
db_path = Path(__file__).resolve().parent / "ev_market.db"
con = sqlite3.connect(db_path)
df = pd.read_csv(csv)
df.to_sql("ev_market", con, if_exists="replace", index=False)
print(f"Stored {len(df):,} rows in table ev_market (database file: {db_path.name})\n")

queries = [
("1. Total rows and distinct manufacturers",
 "SELECT COUNT(*) AS total_rows, COUNT(DISTINCT manufacturer) AS manufacturers, COUNT(DISTINCT category) AS categories FROM ev_market"),
("2. Top 10 manufacturers by total annual sales",
 "SELECT manufacturer, CAST(SUM(annual_sales_units) AS INTEGER) AS total_sales FROM ev_market GROUP BY manufacturer ORDER BY total_sales DESC LIMIT 10"),
("3. Sales and average price by category",
 "SELECT category, COUNT(*) AS models, CAST(SUM(annual_sales_units) AS INTEGER) AS total_sales, ROUND(AVG(price_usd),2) AS avg_price FROM ev_market GROUP BY category ORDER BY total_sales DESC"),
("4. Battery technology comparison",
 "SELECT battery_type, ROUND(AVG(range_km),1) AS avg_range_km, ROUND(AVG(charging_dc_fast_time_min),1) AS avg_fast_charge_min, ROUND(AVG(battery_cycle_life),0) AS avg_cycle_life, ROUND(AVG(battery_degradation_pct_5yr),2) AS avg_degradation_pct FROM ev_market GROUP BY battery_type ORDER BY avg_cycle_life DESC"),
("5. Region-wise performance",
 "SELECT market_region, COUNT(*) AS models, ROUND(AVG(price_usd),0) AS avg_price, ROUND(AVG(customer_rating),2) AS avg_rating FROM ev_market GROUP BY market_region ORDER BY models DESC"),
("6. Year-wise trend",
 "SELECT model_year, COUNT(*) AS models, ROUND(AVG(range_km),1) AS avg_range_km, ROUND(AVG(price_usd),0) AS avg_price FROM ev_market GROUP BY model_year ORDER BY model_year"),
("7. Best value vehicles (km of range per 1000 USD), top 10",
 "SELECT model_name, manufacturer, category, price_usd, range_km, ROUND(range_km*1.0/price_usd*1000,2) AS km_per_1000usd FROM ev_market WHERE price_usd > 0 ORDER BY km_per_1000usd DESC LIMIT 10"),
]
for title, q in queries:
    print("=" * 100); print(title); print("-" * 100); print(q + ";\n")
    print(pd.read_sql_query(q, con).to_string(index=False))
    print(); input("Take a screenshot now, then press Enter for the next query...")

con.execute("DROP VIEW IF EXISTS vw_ev_clean")
con.execute("""CREATE VIEW vw_ev_clean AS SELECT *, ROUND(range_km*1.0/price_usd*1000,2) AS range_per_1000usd,
  CASE WHEN price_usd < 20000 THEN 'Budget' WHEN price_usd < 60000 THEN 'Mid-range'
       WHEN price_usd < 120000 THEN 'Premium' ELSE 'Luxury' END AS price_segment
  FROM ev_market WHERE price_usd > 0 AND range_km > 0""")
print("=" * 100); print("8. Clean view for Tableau: price segments"); print("-" * 100)
print(pd.read_sql_query("SELECT price_segment, COUNT(*) AS models FROM vw_ev_clean GROUP BY price_segment ORDER BY models DESC", con).to_string(index=False))
con.commit(); con.close()
print("\nDone. All queries ran successfully."); input("Press Enter to close...")
