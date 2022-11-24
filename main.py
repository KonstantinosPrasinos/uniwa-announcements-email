import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import smtplib, ssl

load_dotenv()

databaseUrl = os.environ.get("database-url")
databaseKey = os.environ.get("database-key")
senderEmail = os.environ.get("sender-email")
senderPassword = os.environ.get("sender-password")

# Make request to get announcements feed
response = requests.get("http://www.ice.uniwa.gr/feed/")

# Get all items from feed
xml = response.text
root = ET.fromstring(xml)
items = root[0].findall("item")

latestAnnouncementDate = 0
newAnnouncements = []
newAnnouncementsLinks = []

# Get most recent date from file
f = open("latestAnnouncementDate.txt", "r")
readDate = f.read()
f.close()

for child in items:
    date = child.find("pubDate").text
    title = child.find("title").text
    link = child.find("link").text
    dateTimestamp = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z").timestamp()

    if dateTimestamp > float(readDate):
        newAnnouncements.append(title)
        newAnnouncementsLinks.append(link)
        # Only keep the latest date
        if dateTimestamp > latestAnnouncementDate:
            latestAnnouncementDate = dateTimestamp

# Ff no new announcements quit the script
if len(newAnnouncements) == 0:
    quit()

# Else write the latest announcement date to the file
f = open("latestAnnouncementDate.txt", "w")
f.write(str(latestAnnouncementDate))
f.close()

# Get email list from database
Supabase: Client = create_client(databaseUrl, databaseKey)
emailList = Supabase.table("emails").select("*").execute().data

# Format the emails in a list
emailListProper = []
for i in range(0, len(emailList)):
    emailListProper.append(emailList[i]['email'])

def sendEmails():
    subject = str(len(newAnnouncements)) + ' νέες ανακοινώσεις από το ice uniwa'

    # Create the body of the email
    text = ''
    for i in range(1, len(newAnnouncements) + 1):
        text = text + str(i) + ". " + newAnnouncements[i - 1] + "\n" + newAnnouncementsLinks[i - 1] + "\n"

    message = 'Subject: {}\n\n{}'.format(subject, text)

    port = 465
    context = ssl.create_default_context()

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(senderEmail, senderPassword)
        server.sendmail(senderEmail, list(emailListProper), message.encode("utf-8"))
        server.quit()


sendEmails()

