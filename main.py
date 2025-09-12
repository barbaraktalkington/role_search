import gspread
from oauth2client.service_account import ServiceAccountCredentials
import feedparser 



# 1. Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-dab9857c348f.json", scope)
client = gspread.authorize(creds)

# 2. Open your Google Sheet (must match the name you gave it in Drive)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-dab9857c348f.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Job Search Results").sheet1

# 3. Fetch job search results (replace with your actual job search logic)

def fetch_jobs(keyword, location="Seattle, WA"):
    """
    Fetch jobs from Indeed using RSS.
    :param keyword: search keyword (e.g., 'UX Researcher')
    :param location: city/state or 'remote'
    :return: list of job dicts
    """
    base_url = "https://www.indeed.com/rss?q={}&l={}"
    url = base_url.format(keyword.replace(" ", "+"), location.replace(" ", "+"))
    feed = feedparser.parse(url)

    jobs = []
    for entry in feed.entries:
        jobs.append({
            "title": entry.title,
            "company": entry.author if hasattr(entry, "author") else "Unknown",
            "location": location,
            "link": entry.link
        })
    return jobs

# 4. Keywords to include in search
# keywords = ["UX Researcher", "Product Designer", "UX Designer", "UI Designer", "Interaction Designer", "Design Researcher", "Policy Analyst", "Public Service Management","Public Service", "Management", "Consulting", "Consultant", "Manager", "Business Analyst", "Management Consultant", "Strategy Consultant", "Data Analyst", "Data Scientist", "Data Engineer", "Machine Learning Engineer", "AI Specialist"]
keywords = ["UX Researcher", "Design Researcher", "Policy Analyst"]

# 5. Fetch jobs for all keywords
all_jobs = []
for kw in keywords:
    all_jobs.extend(fetch_jobs(kw, location="Seattle, WA"))
    all_jobs.extend(fetch_jobs(kw, location="remote"))

# 6. Write header if sheet is empty
if not sheet.get_all_values():
    sheet.append_row(["Title", "Company", "Location", "Link"])

# 7. Write job results into Google Sheet
jobs = all_jobs
for job in jobs:
    sheet.append_row([job["title"], job["company"], job["location"], job["link"]])

print(f"✅ {len(jobs)} Jobs successfully written to Google Sheet!")
