# 📄 Role Search Automation

This project automates job searches and writes results into a Google Sheet daily.
It currently uses the Remotive API to fetch job postings and logs them into Google Sheets for easy tracking and filtering.

## 🚀 Features
- Fetches real job postings from Remotive | API.
- Automatically writes results to a Google Sheet (Job Search Results).
- Adds dynamic headers (Title, Company, Location, Link, Date Added, Applied?).
- Includes a timestamp (Date Added) for each job.
- Provides an “Applied?” column for manual tracking.
- Prevents duplicates by checking job links.
- Logs progress in the console (🔍 Fetching..., ✅ Found..., ✅ X jobs written).

## 🛠 Setup Instructions
1. Clone the Repo
    ``` bash
    git clone https://github.com/yourusername/role_search.git
    cd role_search
    ```
2. Create Virtual Environment
    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install Dependencies
    ```bash
    pip install gspread oauth2client requests schedule
    ```
4. Set Up Google Sheets Access
    1. Go to Google Cloud Console.
    2. Create a new project (e.g., role-search).
    3. Enable APIs:
        - Google Sheets API
        - Google Drive API
    4. Create Service Account credentials.
        - Download the JSON key file → save it into your repo as role-search-xxxx.json.
    5. Create a new Google Sheet called Job Search Results.
    6. Share it with your service account email (from the JSON file).

## ▶️ Usage
Run the script manually:

```bash
python main.py
```

Console output example:
```pgsql
🔍 Fetching from: https://remotive.com/api/remote-jobs?search=UX Researcher
✅ Found 3 jobs for 'UX Researcher'
✅ 3 new jobs successfully written to Google Sheet!
```

## ⏰ Automation
### Option A: Run Daily with cron
Edit your crontab:
```bash
crontab -e
```

Add this line to run every day at 9 AM:
```0 9 * * * /Users/yourname/role_search/.venv/bin/python /Users/yourname/role_search/main.py
```
### Option B: Run Daily with launchd (macOS)
1. Create ~/Library/LaunchAgents/com.role_search.job.plist.
2. Add a schedule (see main.py docs).
3. Load with:
```bash
launchctl load ~/Library/LaunchAgents/com.role_search.job.plist
```

### 🧭 Roadmap (Future Work)
- Add support for multiple sources (e.g., Greenhouse, Lever, Google Jobs API).
- Add filters (e.g., Seattle-only, exclude certain keywords).
- Send daily email/slack notifications with new job results.
- Track applications & status directly in the sheet.