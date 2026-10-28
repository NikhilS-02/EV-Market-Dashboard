"""Optional: build the cleaned CSV with the same derived fields used in Tableau."""
import pandas as pd

df = pd.read_csv("data/raw/ev_market_test.csv")
c = df[(df.price_usd > 0) & (df.range_km > 0)].copy()
c["range_per_1000usd"] = c.range_km / c.price_usd * 1000
c["price_segment"] = pd.cut(c.price_usd, [0, 20000, 60000, 120000, 1e9],
                            labels=["Budget", "Mid-range", "Premium", "Luxury"], right=False)
c["range_class"] = pd.cut(c.range_km, [0, 250, 450, 1e9], labels=["Short", "Medium", "Long"], right=False)
c["est_revenue_usd"] = c.price_usd * c.annual_sales_units
c.to_csv("data/cleaned/ev_market_clean.csv", index=False)
print("Saved", len(c), "rows")
