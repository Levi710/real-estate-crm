from fastapi import FastAPI
import psycopg2
import json

app = FastAPI()

from dotenv import load_dotenv
import os


# connection
def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL")
       #host="127.0.0.1", port=5433,
       #dbname="realestate_crm", user="admin", password="password"
    )
load_dotenv()          # load .env file
conn = get_connection() # create connection
cur = conn.cursor()     # create cursor

@app.get("/agents")
def get_agents():
    conn = get_connection()
    cur= conn.cursor()
    cur.execute("select * from agents")
    #json 
    columns =[desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return [dict(zip(columns,row)) for row in rows]

@app.get("/properties")
def get_properties():
    conn = get_connection()
    cur= conn.cursor()
    cur.execute("select * from properties")
    #json 
    columns =[desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return [dict(zip(columns,row)) for row in rows]

@app.get("/transactions")
def get_transactions():
    conn = get_connection()
    cur= conn.cursor()
    cur.execute("select * from transactions")
    #json 
    columns =[desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return [dict(zip(columns,row)) for row in rows]
