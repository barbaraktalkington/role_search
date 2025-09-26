print("Job started")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests 
import feedparser
from datetime import datetime

# --- NEW SAFE FETCH WRAPPER ---
def safe_fetch(fetch_func, keyword):
    """Run a fetcher safely. If it errors, return an empty list instead of crashing."""
    try:
        return fetch_func(keyword)
    except Exception as e:
        print(f"⚠️ Error in {fetch_func.__name__} with keyword '{keyword}': {e}")
        return []


# 1. Connect and Open your Google Sheet (must match the name you gave it in Drive)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-dab9857c348f.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Job Search Results").sheet1

#---------------- 2. FETCHERS ---------------- #
 
# Remotive 
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
                "link": job['url'],
                "source": "Remotive"
            })
    #print(f"🔍 Fetching from: {url}")   # <--- debug line
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (Remotive)")  # <--- debug line
    return jobs

# Remote OK
def fetch_jobs_remoteok(keyword):
    url = "https://remoteok.com/api"
    print(f"🔍 Fetching from RemoteOK: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    jobs = []
    for job in data[1:]:  # first element is metadata
        if keyword.lower() in job.get("position", "").lower():
            jobs.append({
                "title": job.get("position"),
                "company": job.get("company"),
                "location": job.get("location", "Remote"),
                "link": job.get("url"),
                "source": "RemoteOK"
            })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (RemoteOK)")
    return jobs

# Working Nomads
def fetch_jobs_workingnomads(keyword):
    url = "https://www.workingnomads.com/api/exposed_jobs"
    print(f"🔍 Fetching from Working Nomads: {url}")
    response = requests.get(url)
    data = response.json()

    jobs = []
    for job in data:
        if keyword.lower() in job.get('title', "").lower():
            jobs.append({
                "title": job('title', ""),
                "company": job.get("company", "Unknown"),
                "location": "Remote",
                "link": job['url'],
                "source": "Working Nomads"
            })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (Working Nomads)")
    return jobs

# We Work Remotely (RSS feed by category)
def fetch_jobs_wwr(keyword):
    # Search all categories: engineering, design, marketing, customer-support, etc.
    categories = ["design", "marketing", "customer-support", "sales", "writing", "product"]
    jobs = []

    for cat in categories:
        url = f"https://weworkremotely.com/categories/remote-{cat}-jobs.rss"
        print(f"🔍 Fetching from WWR: {url}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if keyword.lower() in entry.title.lower():
                jobs.append({
                    "title": entry.title,
                    "company": entry.get("author", "Unknown"),
                    "location": "Remote",
                    "link": entry.link,
                    "source": "We Work Remotely"
                })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (We Work Remotely)")
    return jobs

# PowerToFly
def fetch_jobs_powertofly(keyword):
    url = f"https://powertofly.com/jobs/?keywords={keyword.replace(' ', '+')}"
    print(f"🔍 Fetching from PowerToFly: {url}")
    feed = feedparser.parse(url + "&format=rss")
    jobs = []
    for entry in feed.entries:
        jobs.append({
            "title": entry.title,
            "company": entry.get("author", "Unknown"),
            "location": "Remote",
            "link": entry.link,
            "source": "PowerToFly"
        })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (PowerToFly)")
    return jobs

# Remote.co
def fetch_jobs_remoteco(keyword):
    """Fetch jobs from Remote.co RSS feed."""
    url = f"https://remote.co/remote-jobs/feed/?s={keyword.replace(' ', '+')}"
    print(f"🔍 Fetching from Remote.co: {url}")
    try:
        resp = requests.get(url, timeout=10) # timeout after 10 seconds
        resp.raise_for_status()  # Raise an error for bad status codes
        feed = feedparser.parse(resp.text)
        
        jobs = []
        for entry in feed.entries:
            jobs.append({
                "title": entry.title,
                "company": "Unknown",
                "location": "Remote",
                "link": entry.link,
                "source": "Remote.co"
            })
        print(f"✅ Found {len(jobs)} jobs for '{keyword}' (Remote.co)")
        return jobs
    except Exception as e:
        print(f"⚠️ Error fetching Remote.co jobs: {e}")
        return []

# Jobspresso
def fetch_jobs_jobspresso(keyword):
    url = f"https://jobspresso.co/remote-work/search/{keyword.replace(' ', '+')}/feed/rss2/"
    print(f"🔍 Fetching from Jobspresso: {url}")
    feed = feedparser.parse(url)
    jobs = []
    for entry in feed.entries:
        jobs.append({
            "title": entry.title,
            "company": "Unknown",
            "location": "Remote",
            "link": entry.link,
            "source": "Jobspresso"
        })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (Jobspresso)")
    return jobs

# SkipTheDrive
def fetch_jobs_skipdrive(keyword):
    url = f"https://www.skipthedrive.com/feed/?s={keyword.replace(' ', '+')}"
    print(f"🔍 Fetching from SkipTheDrive: {url}")
    feed = feedparser.parse(url)
    jobs = []
    for entry in feed.entries:
        jobs.append({
            "title": entry.title,
            "company": "Unknown",
            "location": "Remote",
            "link": entry.link,
            "source": "SkipTheDrive"
        })
    print(f"✅ Found {len(jobs)} jobs for '{keyword}' (SkipTheDrive)")
    return jobs
#---------------- END FETCHERS ---------------- #

print("🔁 Fetching jobs...")

# 3. Keywords to include in search
# keywords = ["UX Researcher", "Product Designer", "UX Designer", "UI Designer", "Interaction Designer", "Design Researcher", "Policy Analyst", "Public Service Management","Public Service", "Management", "Consulting", "Consultant", "Manager", "Business Analyst", "Management Consultant", "Strategy Consultant", "Data Analyst", "Data Scientist", "Data Engineer", "Machine Learning Engineer", "AI Specialist"]
keywords = [
    # Existing roles
    "UX Researcher", "Design Researcher", "Policy Analyst",
    # Lazy girl job style
    "Remote Customer Support", "Remote Data Entry", "Remote Virtual Assistant", "Remote Administrative Assistant", "Remote Sales Associate", "Remote Content Writer", "Remote Social Media Manager", "Remote Marketing Coordinator", "Remote Marketing Assistant", "Remote Project Coordinator", "Remote HR Assistant", "Remote HR Coordinator", "Remote Recruiter", "Remote Recruiting Coordinator", "Remote Customer Success", "Remote Data Analyst", "Remote Operations Coordinator", "Remote Community Manager", "Remote Executive Assistant", "Remote Account Manager", "Remote Account Coordinator", "Remote Technical Support", "Remote Help Desk", "Remote Software Tester", "Remote QA Tester", "Remote Quality Assurance", "Remote Content Moderator", "Remote Transcriptionist", "Remote Copywriter", "Remote Proofreader", "Remote Editor"
]


# 4. Fetch jobs for all keywords
all_jobs = []
for kw in keywords:
    all_jobs.extend(safe_fetch(fetch_jobs,kw))               # Remotive
    all_jobs.extend(safe_fetch(fetch_jobs_remoteok, kw))      # RemoteOK
    all_jobs.extend(safe_fetch(fetch_jobs_workingnomads,kw)) # Working Nomads
    all_jobs.extend(safe_fetch(fetch_jobs_wwr,kw))           # We Work Remotely
    all_jobs.extend(safe_fetch(fetch_jobs_powertofly,kw))    # PowerToFly
    all_jobs.extend(safe_fetch(fetch_jobs_remoteco,kw))      # Remote.co
    all_jobs.extend(safe_fetch(fetch_jobs_jobspresso,kw))    # Jobspresso
    all_jobs.extend(safe_fetch(fetch_jobs_skipdrive,kw))     # SkipTheDrive

# 5. Ensure headers exist and add missing ones 
required_headers = ["Title", "Company", "Location", "Link", "Date Added", "Source"]
existing_data = sheet.get_all_values()

if not existing_data:
    sheet.append_row(required_headers)
else:
    current_headers = existing_data[0]
    if current_headers != required_headers:
        # update headers row to match required headers
        sheet.delete_rows(1)
        sheet.insert_row(required_headers, 1)
    print("✅ Header row added checked/updated.")

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

print(f"🔁 Job finished at {datetime.now()}")
print(f"Checked {len(all_jobs)} jobs total, added {new_count} new ones.")

# The following lines are comments to help you check your set up of scheduling job on your Mac using Terminal and launchd.
# --------------------------------------------------------------

## 1. Manually run the job and log at the same time:
# /Users/rara/role_search/.venv/bin/python3 /Users/rara/role_search/main.py >> /Users/rara/role_search/job.log 2>> /Users/rara/role_search/job_error.log
# >> appends terminal output to job.log
# 2>> appends errors to job_error.log
# This simulates what launchd does automatically.
## 2. Check the log after running this:
# cat /Users/rara/role_search/job.log
# cat /Users/rara/role_search/job_error.log
