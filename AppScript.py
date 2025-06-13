import psycopg2
import streamlit as st
from pydantic import BaseModel

conn = psycopg2.connect(
    host = "localhost",
    database = "task_table",
    user = "postgres",
    password = "root",
    port = "5432"
)

cur = conn.cursor()

# Create table if doesn't exit
cur.execute("""
    CREATE TABLE IF NOT EXISTS task_table (
        Task_ID SERIAL PRIMARY KEY,
        Task_Name VARCHAR(255),
        Task_Description TEXT,
        Task_Status VARCHAR(10)
    );
""")
t_id = int(input("Enter the Task ID : "))
t_name = input("Enter the Task Name : ")
t_desc = input("Enter Description of Task: ")
t_status = input("Enter the status of Task : ")

# Insert value
cur.execute("INSERT INTO task_table (Task_ID,Task_Name,Task_Description,Task_Status) values (%s,%s,%s,%s)",(t_id,t_name,t_desc,t_status))

# Committing the Transaction
conn.commit()

# Fetch and display records
cur.execute("Select * from task_table")
rows = cur.fetchall()
for row in rows:
    print(row)

# Closing the database cursor and connection
cur.close()
conn.close()