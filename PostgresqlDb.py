import psycopg2
import streamlit as st
from datetime import date, time

# ✅ PostgreSQL Connection
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="task_table",
        user="postgres",
        password="root",
        port="5432"
    )

conn = get_connection()
cur = conn.cursor()

# ✅ Create Updated Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS task_table (
        Action_Day DATE,
        Task_Name TEXT,
        Start_Time TIME,
        End_Time TIME,
        Language TEXT,
        Platform TEXT
    );
""")
conn.commit()

# ✅ Streamlit UI
st.image("ddtl.png", width=150)
st.title("🛢️ Dual Database Task Logger")
st.subheader("Postgresql Version")

with st.form("task_form"):
    action_day = st.date_input("Action Day", value=date.today())
    task_name = st.text_input("Task Name")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    language = st.text_input("Language")
    platform = st.text_input("Platform")

    submitted = st.form_submit_button("Submit Task")

    if submitted:
        if not task_name.strip():
            st.error("⚠️ Task name is required.")
        elif start_time >= end_time:
            st.error("⚠️ End time must be after start time.")
        else:
            try:
                cur.execute("""
                    INSERT INTO task_table (Action_Day, Task_Name, Start_Time, End_Time, Language, Platform)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (action_day, task_name.strip(), start_time, end_time, language.strip(), platform.strip()))
                conn.commit()
                st.success("✅ Task logged successfully!")
            except Exception as e:
                conn.rollback()
                st.error(f"❌ Database error: {e}")

# ✅ Show All Tasks
st.subheader("📋 All Logged Tasks")

try:
    cur.execute("SELECT * FROM task_table ORDER BY Action_Day DESC, Start_Time ASC")
    rows = cur.fetchall()
    if rows:
        st.table([
            {
                "Date": r[0],
                "Task": r[1],
                "Start": r[2],
                "End": r[3],
                "Language": r[4],
                "Platform": r[5]
            } for r in rows
        ])
    else:
        st.info("No tasks logged yet.")
except Exception as e:
    st.error(f"❌ Error fetching tasks: {e}")
