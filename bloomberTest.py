from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from datetime import datetime

url = 'https://www.bloomberg.com/europe'
page = urlopen(url)
data = []

soup = BeautifulSoup(page, 'html.parser')
contents_box = soup.find('div', attrs={'class': 'highlights-v6__stories'})
eyebrows = contents_box.find_all('a', {'class': 'highlights-v6-story__headline-link'})

for contents in eyebrows:
    title_content = contents.text
    title_link = 'https://www.bloomberg.com' + contents.get('href')
    data.append((title_content, title_link))

print(data)
with open('bloomberg_test1.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for title_content, title_link in data:
        writer.writerow([title_content, title_link, datetime.now()])