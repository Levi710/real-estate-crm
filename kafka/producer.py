from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting Kafka producer...")

for _ in range(10):
    property_data = {
        "title": fake.sentence(nb_words=4),
        "description": fake.text(max_nb_chars=200),
        "property_type": random.choice(['apartment', 'villa', 'plot', 'commercial']),
        "price": round(random.uniform(500000, 10000000), 2),
        "area_sqft": round(random.uniform(500, 5000), 2),
        "city": fake.city(),
        "locality": fake.street_name(),
        "status": random.choice(['available', 'sold', 'rented'])
    }

    producer.send('properties', value=property_data)
    print(f"[PUBLISHED] {property_data['title']} | {property_data['city']} | ₹{property_data['price']}")
    time.sleep(2)

producer.flush()
producer.close()
print("Producer done. 10 properties published.")