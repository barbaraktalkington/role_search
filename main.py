import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests # <-- use requests instead of feedparser
from datetime import datetime

# 1. Connect tand Open your Google Sheet (must match the name you gave it in Drive)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-dab9857c348f.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Job Search Results").sheet1

# 2. Fetch job search results from Remotive API
def fetch_jobs(keyword):
    """
    Fetch jobs from Remotive API.
    :param keyword: search keyword (e.g., 'UX Researcher')
    :param location: city/state or 'remote'
    :return: list of job dicts
    """
    url = f"https://remotive.com/api/remote-jobs?search={keyword}"
    print(f"🔍 Fetching from: {url}")
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


# 3. Keywords to include in search
# keywords = ["UX Researcher", "Product Designer", "UX Designer", "UI Designer", "Interaction Designer", "Design Researcher", "Policy Analyst", "Public Service Management","Public Service", "Management", "Consulting", "Consultant", "Manager", "Business Analyst", "Management Consultant", "Strategy Consultant", "Data Analyst", "Data Scientist", "Data Engineer", "Machine Learning Engineer", "AI Specialist"]
keywords = ["UX Researcher", "Design Researcher", "Policy Analyst"]

# 4. Fetch jobs for all keywords
all_jobs = []
for kw in keywords:
    all_jobs.extend(fetch_jobs(kw))

# 5. Ensure headers exist and add missing ones 
required_headers = ["Title", "Company", "Location", "Link", "Date Added"]
existing_data = sheet.get_all_values()

if not existing_data:
    sheet.append_row(required_headers)
else:
    current_headers = existing_data[0]
    if current_headers != required_headers:
        # update headers row to match required headers
        sheet.delete_rows(1)
        sheet.insert_row(required_headers, 1)
    print("✅ Header row added to Google Sheet!")

# 6. Prevent duplicates based on job link
existing_links = [row[3] for row in sheet.get_all_values()[1:] if len(row) >= 4]

# 7. Append only new job results into Google Sheet
new_count = 0
for job in all_jobs:
    if job["link"] not in existing_links:
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([job["title"], job["company"], job["location"], job["link"], date_added])
        new_count += 1

print(f"✅ {len(all_jobs)} Jobs successfully written to Google Sheet!")
print(f"✅ {new_count} new jobs successfully written to Google Sheet!")
