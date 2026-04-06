from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Database_URL = "mysql+pymysql://root:123%40Deeksha@localhost:3306/deeksha"
engine = create_engine(Database_URL)
Base = declarative_base()
try:
    with engine.connect() as conn:
        print("✅ Connected successfully!")
except Exception as e:
    print("❌ Error:", e)