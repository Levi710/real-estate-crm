# run this once in terminal
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
with open("schema.sql", "r") as f:
    cur.execute(f.read())
conn.commit()
cur.close()
conn.close()
print("Schema created!")