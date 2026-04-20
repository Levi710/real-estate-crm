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

# ── DYNAMIC ANALYTICS SEARCH ─────────────────────────
st.subheader("🔎 Dynamic Data Explorer")

tab1, tab2, tab3 = st.tabs(["Properties", "Agents", "Clients"])

# ── PROPERTIES TAB ───────────────────────────────────
with tab1:
    df_props = run_query("SELECT * FROM properties")
    
    col1, col2, col3 = st.columns(3)
    
    city_options = ["All"] + sorted(df_props["city"].dropna().unique().tolist())
    type_options = ["All"] + sorted(df_props["property_type"].dropna().unique().tolist())
    status_options = ["All"] + sorted(df_props["status"].dropna().unique().tolist())
    
    selected_city   = col1.selectbox("City", city_options)
    selected_type   = col2.selectbox("Property Type", type_options)
    selected_status = col3.selectbox("Status", status_options)
    
    price_min, price_max = st.slider(
        "Price Range (₹)",
        min_value=int(df_props["price"].min()),
        max_value=int(df_props["price"].max()),
        value=(int(df_props["price"].min()), int(df_props["price"].max()))
    )
    
    filtered = df_props.copy()
    if selected_city   != "All": filtered = filtered[filtered["city"] == selected_city]
    if selected_type   != "All": filtered = filtered[filtered["property_type"] == selected_type]
    if selected_status != "All": filtered = filtered[filtered["status"] == selected_status]
    filtered = filtered[(filtered["price"] >= price_min) & (filtered["price"] <= price_max)]
    
    st.markdown(f"**{len(filtered)} properties found**")
    st.dataframe(filtered[["title", "property_type", "city", "locality", "price", "area_sqft", "status"]])

# ── AGENTS TAB ───────────────────────────────────────
with tab2:
    df_agents = run_query("SELECT * FROM agents")
    
    search_name = st.text_input("Search agent by name")
    active_filter = st.radio("Status", ["All", "Active", "Inactive"], horizontal=True)
    
    filtered_agents = df_agents.copy()
    if search_name:
        filtered_agents = filtered_agents[filtered_agents["full_name"].str.contains(search_name, case=False)]
    if active_filter == "Active":
        filtered_agents = filtered_agents[filtered_agents["is_active"] == True]
    elif active_filter == "Inactive":
        filtered_agents = filtered_agents[filtered_agents["is_active"] == False]
    
    st.markdown(f"**{len(filtered_agents)} agents found**")
    st.dataframe(filtered_agents[["full_name", "email", "phone", "license_number", "hire_date", "is_active"]])

# ── CLIENTS TAB ──────────────────────────────────────
with tab3:
    df_clients_data = run_query("SELECT * FROM clients")
    
    search_client = st.text_input("Search client by name")
    type_filter = st.radio("Client Type", ["All", "buyer", "seller", "both"], horizontal=True)
    
    filtered_clients = df_clients_data.copy()
    if search_client:
        filtered_clients = filtered_clients[filtered_clients["full_name"].str.contains(search_client, case=False)]
    if type_filter != "All":
        filtered_clients = filtered_clients[filtered_clients["client_type"] == type_filter]
    
    st.markdown(f"**{len(filtered_clients)} clients found**")
    st.dataframe(filtered_clients[["full_name", "email", "phone", "client_type", "created_at"]])


    import plotly.express as px

# ── ADVANCED ANALYTICS ───────────────────────────────
st.subheader("📈 Advanced Analytics")

col1, col2 = st.columns(2)

# ── PIE CHART — Property Type Distribution ───────────
with col1:
    df_pie = run_query("""
        SELECT property_type, COUNT(*) as count
        FROM properties GROUP BY property_type
    """)
    fig1 = px.pie(df_pie, names="property_type", values="count",
                  title="Property Type Distribution",
                  color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig1, use_container_width=True)

# ── PIE CHART — Payment Mode ─────────────────────────
with col2:
    df_pay = run_query("""
        SELECT payment_mode, COUNT(*) as count
        FROM transactions GROUP BY payment_mode
    """)
    fig2 = px.pie(df_pay, names="payment_mode", values="count",
                  title="Payment Mode Distribution",
                  color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# ── BAR CHART — Listings by Status ───────────────────
with col3:
    df_lst = run_query("""
        SELECT status, COUNT(*) as count
        FROM listings GROUP BY status
    """)
    fig3 = px.bar(df_lst, x="status", y="count",
                  title="Listings by Status",
                  color="status",
                  color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig3, use_container_width=True)

# ── BAR CHART — Leads by Interest Level ──────────────
with col4:
    df_leads = run_query("""
        SELECT interest_level, COUNT(*) as count
        FROM leads GROUP BY interest_level
    """)
    fig4 = px.bar(df_leads, x="interest_level", y="count",
                  title="Leads by Interest Level",
                  color="interest_level",
                  color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig4, use_container_width=True)

# ── SCATTER PLOT — Price vs Area ─────────────────────
st.subheader("💰 Price vs Area Analysis")
df_scatter = run_query("""
    SELECT title, price, area_sqft, property_type, city
    FROM properties
""")
fig5 = px.scatter(df_scatter, x="area_sqft", y="price",
                  color="property_type", hover_data=["title", "city"],
                  title="Property Price vs Area (sqft)",
                  labels={"area_sqft": "Area (sqft)", "price": "Price (₹)"},
                  color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig5, use_container_width=True)

# ── LINE CHART — Transactions Over Time ──────────────
st.subheader("📅 Transaction Trend")
df_trend = run_query("""
    SELECT DATE_TRUNC('month', transaction_date) as month,
    COUNT(*) as total, SUM(final_price) as revenue
    FROM transactions
    GROUP BY month ORDER BY month
""")
fig6 = px.line(df_trend, x="month", y="revenue",
               title="Monthly Revenue Trend",
               labels={"month": "Month", "revenue": "Revenue (₹)"},
               markers=True,
               color_discrete_sequence=["#2d4a3e"])
st.plotly_chart(fig6, use_container_width=True)

# ── HEATMAP — Agent x Interaction Type ───────────────
st.subheader("🤝 Agent Interaction Heatmap")
df_heat = run_query("""
    SELECT a.full_name, i.interaction_type, COUNT(*) as count
    FROM interactions i
    JOIN agents a ON i.agent_id = a.id
    GROUP BY a.full_name, i.interaction_type
""")
df_pivot = df_heat.pivot(index="full_name", columns="interaction_type", values="count").fillna(0)
fig7 = px.imshow(df_pivot,
                 title="Agent Interaction Heatmap",
                 color_continuous_scale="Teal",
                 aspect="auto")
st.plotly_chart(fig7, use_container_width=True)