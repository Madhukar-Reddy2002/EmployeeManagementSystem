from datetime import datetime

departments = ["Engineering", "Sales", "Marketing", "Finance", "Human Resources"]
job_titles = ["Software Engineer", "Sales Representative", "Marketing Manager", "Financial Analyst", "HR Coordinator"]

def get_departments():
    return departments

def get_job_titles():
    return job_titles

def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")