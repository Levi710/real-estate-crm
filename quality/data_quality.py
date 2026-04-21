import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def run_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

print("=== Data Quality Report ===\n")

# AGENTS
total_agents = run_query("SELECT COUNT(*) FROM agents")
missing_emails = run_query("SELECT COUNT(*) FROM agents WHERE email IS NULL")
duplicate_emails = run_query("SELECT COUNT(*) - COUNT(DISTINCT email) FROM agents")

print(f"[agents]")
print(f"- Total rows: {total_agents}")
print(f"- Missing emails: {missing_emails}")
print(f"- Duplicate emails: {duplicate_emails}\n")

# PROPERTIES 
total_properties  = run_query("SELECT COUNT(*) FROM properties")
negative_prices  = run_query("SELECT COUNT(*) FROM properties WHERE price < 0")
invalid_type = run_query("SELECT COUNT(*) FROM properties WHERE property_type NOT IN ('apartment','villa','plot','commercial')")
invalid_status = run_query("SELECT COUNT(*) FROM properties WHERE status NOT IN ('available','sold','rented')")

print(f"[properties]")
print(f"- Total rows: {total_properties}")
print(f"- Negative prices: {negative_prices}")
print(f"- Invalid property_type: {invalid_type}")
print(f"- Invalid status: {invalid_status}\n")


# CLIENTS
# CLIENTS
total_clients = run_query("SELECT COUNT(*) FROM clients")
missing_emails_clients = run_query("SELECT COUNT(*) FROM clients WHERE email IS NULL")
invalid_client_type = run_query("SELECT COUNT(*) FROM clients WHERE client_type NOT IN ('buyer','seller','both')")

print(f"[clients]")
print(f"- Total rows: {total_clients}")
print(f"- Missing emails: {missing_emails_clients}")
print(f"- Invalid client_type: {invalid_client_type}\n")

print("=== Report Complete ===")