import sqlite3
import streamlit as st
import pandas as pd
from utils import get_departments, get_job_titles
from streamlit.runtime.caching import cache_resource
import datetime

@cache_resource
def get_connection():
   return sqlite3.connect('employee_data.db', check_same_thread=False)

def init_db():
   conn = get_connection()
   conn.execute("""
       CREATE TABLE IF NOT EXISTS employees (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           email TEXT UNIQUE NOT NULL,
           department TEXT NOT NULL,
           job_title TEXT NOT NULL,
           hire_date TEXT NOT NULL,
           salary REAL NOT NULL
       )
   """)
   conn.commit()

def fetch_employees():
   conn = get_connection()
   return conn.execute("SELECT * FROM employees").fetchall()

def add_employee():
   departments = get_departments()
   job_titles = get_job_titles()

   name = st.text_input("Name")
   email = st.text_input("Email")
   department = st.selectbox("Department", departments)
   job_title = st.selectbox("Job Title", job_titles)
   hire_date = st.date_input("Hire Date")
   salary = st.number_input("Salary", min_value=0.0, step=1000.0, format="%.2f")

   if st.button("Add Employee"):
       conn = get_connection()
       conn.execute("INSERT INTO employees (name, email, department, job_title, hire_date, salary) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, email, department, job_title, hire_date, salary))
       conn.commit()
       st.success(f"Employee {name} added successfully!")

def get_employee(employee_id):
   conn = get_connection()
   c = conn.cursor()
   c.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
   employee = c.fetchone()
   c.close()
   return employee

def update_employee():
   employee_id = st.text_input("Enter Employee ID")

   if st.button("Get Employee Details"):
       employee = get_employee(employee_id)

       if employee:
           departments = get_departments()
           job_titles = get_job_titles()

           name = st.text_input("Name", value=employee[1])
           email = st.text_input("Email", value=employee[2])
           department = st.selectbox("Department", departments, index=departments.index(employee[3]))
           job_title = st.selectbox("Job Title", job_titles, index=job_titles.index(employee[4]))
           hire_date = st.date_input("Hire Date", value=datetime.date.fromisoformat(employee[5]))
           salary = st.number_input("Salary", min_value=0.0, step=1000.0, format="%.2f", value=float(employee[6]))

           # Use a button to trigger the update
           update_state = st.button("Update Employee")

           if update_state:
               conn = get_connection()
               conn.execute("UPDATE employees SET name = ?, email = ?, department = ?, job_title = ?, hire_date = ?, salary = ? WHERE id = ?",
                            (name, email, department, job_title, hire_date, salary, employee_id))
               conn.commit()
               st.success("Employee information updated successfully!")
       else:
           st.warning("Employee not found.")

def search_employees():
   search_query = st.text_input("Search by Name or Department")

   if st.button("Search"):
       conn = get_connection()
       c = conn.cursor()
       c.execute("SELECT * FROM employees WHERE name LIKE ? OR department LIKE ?", (f"%{search_query}%", f"%{search_query}%"))
       employees = c.fetchall()
       c.close()

       if employees:
           employees_df = pd.DataFrame(employees, columns=["ID", "Name", "Email", "Department", "Job Title", "Hire Date", "Salary"])
           st.dataframe(employees_df)
       else:
           st.warning("No employees found.")

def get_salary_stats():
   conn = get_connection()
   c = conn.cursor()
   c.execute("SELECT AVG(salary) AS average_salary, MAX(salary) AS highest_salary, MIN(salary) AS lowest_salary FROM employees")
   salary_stats = c.fetchone()

   c.execute("SELECT department, AVG(salary) AS average_salary FROM employees GROUP BY department")
   dept_salaries = c.fetchall()
   c.close()

   return salary_stats + (dept_salaries,)