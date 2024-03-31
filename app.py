import streamlit as st
import pandas as pd
from db import init_db, get_connection, fetch_employees, add_employee, get_employee, update_employee, search_employees, get_salary_stats
from utils import format_date

# Set page config at the start
st.set_page_config(page_title="Employee Management System", page_icon=":briefcase:", layout="wide")

init_db()  # Initialize the database
st.title("Employee Management System")

# Create a sidebar for navigation
menu = ["Dashboard", "Add Employee", "View Employees", "Employee Details", "Update Employee", "Search Employees", "Salary Analytics"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Dashboard":
    st.subheader("Employee Dashboard")
    employees = fetch_employees()
    if employees:
        employees_df = pd.DataFrame(employees, columns=["ID", "Name", "Email", "Department", "Job Title", "Hire Date", "Salary"])
        employees_df["Hire Date"] = employees_df["Hire Date"].apply(format_date)
        employees_df = employees_df.fillna("N/A")  # Handle null values

        # Interactive filters
        dept_filter = st.multiselect("Filter by Department", employees_df["Department"].unique())
        job_filter = st.multiselect("Filter by Job Title", employees_df["Job Title"].unique())

        # Apply filters
        filtered_df = employees_df.copy()
        if dept_filter:
            filtered_df = filtered_df[filtered_df["Department"].isin(dept_filter)]
        if job_filter:
            filtered_df = filtered_df[filtered_df["Job Title"].isin(job_filter)]

        st.dataframe(filtered_df)
    else:
        st.warning("No employees found.")

elif choice == "Add Employee":
    st.subheader("Add New Employee")
    add_employee()

elif choice == "View Employees":
    st.subheader("Employee List")
    employees = fetch_employees()
    employees_df = pd.DataFrame(employees, columns=["ID", "Name", "Email", "Department", "Job Title", "Hire Date", "Salary"])
    employees_df["Hire Date"] = employees_df["Hire Date"].apply(format_date)
    employees_df = employees_df.fillna("N/A")  # Handle null values
    st.dataframe(employees_df)

elif choice == "Employee Details":
    st.subheader("Employee Details")
    employee_id = st.text_input("Enter Employee ID")
    if st.button("Get Details"):
        employee = get_employee(employee_id)
        if employee:
            st.write(f"**Name:** {employee[1]}")
            st.write(f"**Email:** {employee[2]}")
            st.write(f"**Department:** {employee[3]}")
            st.write(f"**Job Title:** {employee[4]}")
            st.write(f"**Hire Date:** {format_date(employee[5])}")
            st.write(f"**Salary:** ${employee[6]:.2f}")
        else:
            st.warning("Employee not found.")

elif choice == "Update Employee":
    st.subheader("Update Employee Information")
    update_employee()

elif choice == "Search Employees":
    st.subheader("Search Employees")
    search_employees()

elif choice == "Salary Analytics":
    st.subheader("Salary Analytics")
    salary_stats = get_salary_stats()
    st.write(f"**Average Salary:** ${salary_stats[0]:.2f}")
    st.write(f"**Highest Salary:** ${salary_stats[1]:.2f}")
    st.write(f"**Lowest Salary:** ${salary_stats[2]:.2f}")
    st.subheader("Average Salary by Department")
    dept_salaries = salary_stats[3]
    dept_salaries_df = pd.DataFrame(dept_salaries, columns=["Department", "Average Salary"])
    dept_salaries_df = dept_salaries_df.fillna("N/A")
    st.dataframe(dept_salaries_df)