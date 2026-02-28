import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def search_jobs():
    query = "entry level data analyst startup jobs apply India"
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url).json()

    jobs = []
    related = response.get("RelatedTopics", [])

    for item in related[:10]:
        if "Text" in item and "FirstURL" in item:
            jobs.append({
                "title": item["Text"],
                "link": item["FirstURL"]
            })

    return jobs

def send_email(jobs):
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    receiver = "farshanam2907@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Entry Level Data Analyst Jobs"
    message["From"] = sender
    message["To"] = receiver

    html = "<h2>Top 10 Entry-Level Data Analyst Startup Jobs</h2><ul>"
    for job in jobs:
        html += f"<li><a href='{job['link']}'>{job['title']}</a></li>"
    html += "</ul>"

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())

if __name__ == "__main__":
    jobs = search_jobs()
    if jobs:
        send_email(jobs)