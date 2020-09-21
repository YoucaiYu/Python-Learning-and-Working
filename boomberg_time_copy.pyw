import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import csv
from datetime import datetime

scheduler = BlockingScheduler()

def my_scrabling_job():
    url = 'https://www.bloomberg.com/europe'
    page = urlopen(url)
    data = []

    soup = BeautifulSoup(page, 'html.parser')
    contents_box = soup.find('div', attrs={'class': 'home__top-of-home'})
    all_titles = contents_box.find_all('a')

    for titles in all_titles:
        name = titles.text
        link = titles.get('href')

        if name == 'Share on Facebook':
            continue
        elif name == 'Share on Twitter':
            continue
        elif name == 'Subscribe':
            continue
        new_link = urljoin(url, link)
        data.append((name, new_link))

    # with newline can delete space rów in the csv
    with open('bloomberg_test4.csv', 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for name, new_link in data:
            rows = [name, new_link, datetime.now()]
            writer.writerow(rows)

scheduler.add_job(my_scrabling_job, 'cron', minute='*/15', hour='9-17', day_of_week='0-6')
scheduler.start()