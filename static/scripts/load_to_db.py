"""Load the Skill Wallet EV dataset into MySQL.
Usage:  python scripts/load_to_db.py
Requires a .env file (see .env.example) and the database created via sql/schema.sql
"""
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
url = "mysql+pymysql://{u}:{p}@{h}:{port}/{db}".format(
    u=os.getenv("DB_USER", "root"), p=os.getenv("DB_PASSWORD", ""),
    h=os.getenv("DB_HOST", "localhost"), port=os.getenv("DB_PORT", "3306"),
    db=os.getenv("DB_NAME", "ev_db"))
engine = create_engine(url)

df = pd.read_csv("data/raw/ev_market_test.csv")
df.to_sql("ev_market", engine, if_exists="replace", index=False, chunksize=5000)
print(f"Loaded {len(df):,} rows into ev_market")
