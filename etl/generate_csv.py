import pandas as pd
import random
from faker import Faker

fake = Faker()

# new_clients.csv
clients = []
for _ in range(10):
    clients.append({
        "full_name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number()[:15],
        "client_type": random.choice(['buyer','seller','both'])
    })

# inject dirty data
clients[3]["client_type"] ="unknown" #invalid enum
clients[7]["phone"] = "" #missing phone

df_clients = pd.DataFrame(clients)
df_clients.to_csv("data/new_clients.csv", index=False)
print("new_clients.csv created")

# new_properties.csv

properties =[]
for _ in range(10):
    properties.append({
        "title": fake.sentence(nb_words=4),
        "description": fake.text(max_nb_chars=200),
        "property_type": random.choice(['apartment','villa', 'plot', 'commercial',]),
        "price": round(random.uniform(500000,10000000),2),
        "area_sqft": round(random.uniform(500,5000),2),
        "city": fake.city(),
        "locality": fake.street_name(),
        "status": random.choice(['available','sold','rented'])
    })

# inject dirty data
properties[2]["city"]= "" #missing city
properties[5]["price"]= -999999 #invalid price
properties[8]["status"]= "unknow" #invalid enum

df_properties =pd.DataFrame(properties)
df_properties.to_csv("data/new_properties.csv",index=False)
print("new_properties.csv created")
