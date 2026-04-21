from kafka import KafkaConsumer
import psycopg2
import json
from dotenv import load_dotenv
import os

load_dotenv()

consumer = KafkaConsumer(
    'properties',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

print("Starting Kafka consumer... waiting for messages")

for message in consumer:
    prop = message.value
    print(f"[RECEIVED] {prop['title']} | {prop['city']}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO properties (title, description, property_type, price, area_sqft, city, locality, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        prop['title'],
        prop['description'],
        prop['property_type'],
        prop['price'],
        prop['area_sqft'],
        prop['city'],
        prop['locality'],
        prop['status']
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[INSERTED] {prop['title']} into PostgreSQL")