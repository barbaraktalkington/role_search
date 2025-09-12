import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests # <-- use requests instead of feedparser
from datetime import datetime

# 1. Connect tand Open your Google Sheet (must match the name you gave it in Drive)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-dab9857c348f.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Job Search Results").sheet1

# 3. Fetch job search results from Remotive API
def fetch_jobs(keyword):
    """
    Fetch jobs from Remotive API.
    :param keyword: search keyword (e.g., 'UX Researcher')
    :param location: city/state or 'remote'
    :return: list of job dicts
    """
    url = f"https://remotive.com/api/remote-jobs?search={keyword}"
    response = requests.get(url)
    data = response.json()
   
    jobs = []
    for job in data['jobs']:
        jobs.append({
                "title": job['title'],
                "company": job['company_name'],
                "location": job['candidate_required_location'],
                "link": job['url']
            })
    #print(f"🔍 Fetching from: {url}")   # <--- debug line
    print(f"✅ Found {len(jobs)} jobs for '{keyword}'")  # <--- debug line
    return jobs


# 4. Keywords to include in search
# keywords = ["UX Researcher", "Product Designer", "UX Designer", "UI Designer", "Interaction Designer", "Design Researcher", "Policy Analyst", "Public Service Management","Public Service", "Management", "Consulting", "Consultant", "Manager", "Business Analyst", "Management Consultant", "Strategy Consultant", "Data Analyst", "Data Scientist", "Data Engineer", "Machine Learning Engineer", "AI Specialist"]
keywords = ["UX Researcher", "Design Researcher", "Policy Analyst"]

# 5. Fetch jobs for all keywords
all_jobs = []
for kw in keywords:
    all_jobs.extend(fetch_jobs(kw))

# 6. Write header if sheet is empty
if not sheet.get_all_values():
    sheet.append_row(["Title", "Company", "Location", "Link", "Date Added"])

# 7. Write job results into Google Sheet
jobs = all_jobs
for job in jobs:
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([job["title"], job["company"], job["location"], job["link"], date_added])

print(f"✅ {len(jobs)} Jobs successfully written to Google Sheet!")
