import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("role-search-603a3ce54f29.json", scope)
client = gspread.authorize(creds)

# 2. Open your Google Sheet (must match the name you gave it in Drive)
sheet = client.open("Job Search Results").sheet1

# 3. Example data (later we’ll replace with real job searches)
jobs = [
    {"title": "UX Researcher", "company": "Meta", "location": "Remote", "link": "http://example.com"},
    {"title": "Policy Analyst", "company": "City of Seattle", "location": "Seattle, WA", "link": "http://example.com"},
]

# 4. Write header if sheet is empty
if not sheet.get_all_values():
    sheet.append_row(["Title", "Company", "Location", "Link"])

# 5. Write job results
for job in jobs:
    sheet.append_row([job["title"], job["company"], job["location"], job["link"]])

print("✅ Jobs successfully written to Google Sheet!")