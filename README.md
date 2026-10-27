# Global Electric Vehicle Market Analysis (SQL + Tableau + Flask)

SmartBridge Skill Wallet project: Data Analytics with Tableau.

Analysis of 100,000 EV models (2018 to 2026): sales, pricing, range, battery technology, regions and CO2 impact.

## Project flow
1. Problem understanding (docs/EV_Market_Tableau_Project_Report.pdf)
2. Data collection: `data/raw/ev_market_test.csv` (provided by Skill Wallet)
3. Store in MySQL: `scripts/load_to_db.py`
4. SQL operations: `sql/queries.sql`
5. Connect MySQL to Tableau, prepare data, build 12 visualizations, 3 dashboards, 6-scene story: `docs/tableau_build_guide.md`
6. Performance testing: `docs/performance_testing.md`
7. Web integration: Flask app embedding the Tableau Public dashboard and story
8. Demo video and documentation

## Run it
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env   then edit values

# 1) create DB:   run sql/schema.sql in MySQL
# 2) load data:
python scripts/load_to_db.py
# 3) run queries from sql/queries.sql in MySQL Workbench
# 4) build the Tableau workbook, publish to Tableau Public, paste URLs into .env
# 5) start the web app:
python app.py                  # http://127.0.0.1:5000
```

## Repo structure
```
app.py                  Flask app (routes: /, /dashboard, /story, /about)
templates/, static/     UI
sql/                    schema + queries + clean view
scripts/                load_to_db.py, clean_data.py
data/raw, data/cleaned  dataset
tableau/                put your .twbx workbook here
docs/                   report PDF, charts, build guide, performance record
```

## Links (fill in)
- Tableau Public dashboard: ADD LINK
- Demo video: ADD LINK

## Note on the data
The dataset is synthetic: models listed per year, regional totals and battery range are almost uniform.
Summed `annual_sales_units` (about 773 million) and estimated revenue are not real-world totals; treat them as relative measures.
