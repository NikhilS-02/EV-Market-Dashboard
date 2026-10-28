-- Run once in MySQL Workbench / CLI
CREATE DATABASE IF NOT EXISTS ev_db;
USE ev_db;
-- The table ev_market is created automatically by scripts/load_to_db.py
-- (pandas.to_sql). Optional: add indexes after loading to speed up Tableau.
-- CREATE INDEX idx_category ON ev_market(category(50));
-- CREATE INDEX idx_year ON ev_market(model_year);
-- CREATE INDEX idx_region ON ev_market(market_region(50));
