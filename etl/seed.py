import psycopg2
import random
from faker import Faker

fake = Faker()

#connect
conn = psycopg2.connect(
    host ="127.0.0.1",
    port=5433,
    dbname="realestate_crm",
    user="admin",
    password="password"
)
cur = conn.cursor()

#agents
for _ in range(10):
    cur.execute("""
        INSERT INTO agents (full_name,email,phone,license_number,hire_date,is_active)
        VALUES (%s, %s,%s,%s,%s,%s)       
""", (
    fake.name(),
    fake.unique.email(),
    fake.phone_number()[:15],
    fake.unique.bothify(text='LIC-#####'),
    fake.date_between(start_date='-5y', end_date='today'),
    random.choice([True, False])
))
    
# fetch agent IDs
cur.execute("SELECT id FROM agents")
agent_ids = [row[0] for row in cur.fetchall()]
print(f"Agents inserted: {len(agent_ids)}")

#clients

for _ in range(50):
    cur.execute("""
        INSERT INTO clients (full_name,email,phone,client_type)
        VALUES (%s,%s,%s,%s)
""", (
    fake.name(),
    fake.unique.email(),
    fake.phone_number()[:15],
    random.choice(['buyer','seller','both'])
))
    
cur.execute("SELECT id FROM clients")
client_ids = [row[0] for row in cur.fetchall()]
print(f"Clients inserted: {len(client_ids)}")

#properties

for _ in range(30):
    cur.execute("""
        INSERT INTO properties (title ,description ,property_type ,price ,area_sqft ,city ,locality ,status)
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

cur.execute("SELECT id from properties")
property_ids= [row[0] for row in cur.fetchall()]
print(f"Properties inserted: {len(property_ids)}")

#listings

for _ in range(30):
    cur.execute("""
        INSERT INTO listings (property_id,agent_id,seller_id,list_price,status)
        VALUES (%s, %s, %s, %s, %s)
""", (
    random.choice(property_ids),
    random.choice(agent_ids),
    random.choice(client_ids),
    round(random.uniform(500000, 10000000), 2),
    random.choice(['active', 'expired' , 'sold'])
))
    
cur.execute("SELECT id from listings")
listing_ids= [row[0] for row in cur.fetchall()]
print(f"Listings inserted : {len(listing_ids)}")

#leads

for _ in range(50):
    cur.execute("""
            INSERT INTO leads (property_id,agent_id,client_id,interest_level,notes)
            VALUES (%s, %s, %s, %s, %s)                   
""", (
     random.choice(property_ids),
     random.choice(agent_ids),
     random.choice(client_ids),
     random.choice(['low','medium','high']),
     fake.text(max_nb_chars=150)
))

cur.execute("SELECT id from leads")
lead_ids= [row[0] for row in cur.fetchall()]
print(f"Leads inserted :{len(lead_ids)}")

#transactions

for _ in range(20):
    cur.execute("""
        INSERT INTO transactions (listing_id,buyer_id,agent_id,final_price,payment_mode)
        VALUES (%s, %s, %s, %s, %s)
""", (
     random.choice(listing_ids),
     random.choice(client_ids),
     random.choice(agent_ids),
     round(random.uniform(500000, 10000000), 2),
     random.choice(['cash','loan','cheque'])
))

cur.execute("SELECT id from transactions")
transaction_ids=[row[0] for row in cur.fetchall()]
print(f"Transaction inserted : {len(transaction_ids)}")

#interactions

for _ in range(60):
    cur.execute("""
        INSERT INTO interactions(agent_id,client_id,interaction_type,notes)
        VALUES (%s, %s, %s, %s)
""", (
     random.choice(agent_ids),
     random.choice(client_ids),
     random.choice(['call', 'email', 'visit']),
     fake.text(max_nb_chars=150)
))

cur.execute("SELECT id from interactions")
interaction_ids = [row[0] for row in cur.fetchall()]
print(f"Interactions inserted : {len(interaction_ids)}")

conn.commit()