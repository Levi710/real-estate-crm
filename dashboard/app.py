import streamlit as st
import psycopg2
import pandas as pd


# connection
def get_connection():
    return psycopg2.connect(
        host="127.0.0.1", port=5433,
        dbname="realestate_crm", user="admin", password="password"
    )

# page config
st.set_page_config(page_title="Real Estate CRM", layout="wide")
st.title("🏠 Real Estate CRM Dashboard")
st.markdown("Analytics dashboard for real estate agents, clients, and transactions.")

# connection
def run_query(query):
    conn = get_connection()
    df= pd.read_sql(query, conn)
    conn.close()
    return df

# KPI CARDS
st.subheader("📊 Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Agents",      run_query("SELECT COUNT(*) FROM agents").iloc[0,0])
col2.metric("Total Clients",     run_query("SELECT COUNT(*) FROM clients").iloc[0,0])
col3.metric("Total Properties",  run_query("SELECT COUNT(*) FROM properties").iloc[0,0])
col4.metric("Total Transactions",run_query("SELECT COUNT(*) FROM transactions").iloc[0,0])


# Top agents by listings:
st.subheader("🏆 Top 5 Agents by Listings")
df1 = run_query("""
    select a.full_name, count(l.id) as total_listings
    from agents a join listings l on a.id = l.agent_id
    group by a.full_name order by total_listings desc limit 5
""")
st.bar_chart(df1.set_index("full_name"))

#Avg price by city:
st.subheader("🏙️ Average Property Price by City")
df2 = run_query("""
    select city, round(avg(price),2) as avg_price
    from properties group by city order by avg_price desc limit 5
""")
st.bar_chart(df2.set_index("city"))

#Lead conversion table:
st.subheader("🎯 Lead Conversion per Property")
df3 = run_query("""
    select p.title, count(distinct l.id) as total_leads,
    count(distinct t.id) as total_transactions
    from properties p
    left join leads l on p.id = l.property_id
    left join listings k on p.id = k.property_id
    left join transactions t on k.id = t.listing_id
    group by p.title order by total_leads desc limit 10
""")
st.dataframe(df3)