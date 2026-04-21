import psycopg2
import pandas as pd

from dotenv import load_dotenv
import os


# connection
def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL")
       #host="127.0.0.1", port=5433,
       #dbname="realestate_crm", user="admin", password="password"
    )
load_dotenv()
conn = get_connection()
cur = conn.cursor()

# extract

df_clients = pd.read_csv("/opt/airflow/data/new_clients.csv")
df_properties= pd.read_csv("/opt/airflow/data/new_properties.csv")

print(f"Clients before cleaning: {len(df_clients)}")
print(f"Properties before cleaning: {len(df_properties)}")

# transform(clients)
valid_types =['buyer','seller', 'both']
df_clients = df_clients[df_clients["client_type"].isin(valid_types)]

df_clients["phone"]= df_clients["phone"].replace("",None)

print(f"Clients after cleaning: {len(df_clients)}")

# transform(properties)

df_properties =df_properties[df_properties["city"] != ""]
df_properties =df_properties[df_properties["price"]>=0]
valid_status = ['available','sold','rented']
df_properties = df_properties[df_properties["status"].isin(valid_status)]
print(f"Properties after cleaning: {len(df_properties)}")

# load(clients)
for _, row in df_clients.iterrows():
    cur.execute("""
        INSERT INTO clients (full_name, email, phone, client_type)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
""", (
    row["full_name"],
    row["email"],
    row["phone"] if row["phone"] else None,
    row["client_type"]
))

print(f"Clients loaded : {len(df_clients)}")

# load(properties)
for _, row in df_properties.iterrows():
    cur.execute("""
        INSERT INTO properties (title,description,property_type,price,area_sqft,city,locality,status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING

""", (
    row["title"],
    row["description"],
    row["property_type"],
    row["price"],
    row["area_sqft"],
    row["city"],
    row["locality"],
    row["status"]
))
    
print(f"Properties loaded : {len(df_properties)}")

conn.commit()
cur.close()
conn.close()
print("ETL pipeline complete!")

