from faker import Faker
from datetime import datetime
import random
from dotenv import load_dotenv
import os
import time
import psycopg2

fake = Faker()
load_dotenv()


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
   

def stream_properties():
    print("Starting real-time property stream...")
    count = 0 
    while count < 12:
        conn = get_connection()
        cur = conn.cursor()
    
        cur.execute("""
        INSERT INTO properties (title, description, property_type, price, area_sqft, city, locality, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        fake.sentence(nb_words=4),
        fake.text(max_nb_chars=200),
        random.choice(['apartment','villa','plot','commercial']),
        round(random.uniform(500000,10000000),2),
        round(random.uniform(500, 5000),2),
        fake.city(),
        fake.street_name(),
        random.choice(['available', 'sold', 'rented'])
    ))
    
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now()}] New property added")
        time.sleep(5)
        count += 1
stream_properties()
print("Stream complete. 12 properties added.")