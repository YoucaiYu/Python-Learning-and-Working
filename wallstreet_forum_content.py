from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

forum_link = pd.read_csv('Wallstreet_link.csv', header=None)
forum_link_list = forum_link[0]

data_list = []
m = 0

for needed_link in forum_link_list:

    forum_content_page = requests.get(needed_link, headers=headers).content
    forum_content_page_soup = BeautifulSoup(forum_content_page, "html.parser")

    posting_contents = forum_content_page_soup.find_all('div', attrs={'posting'})

    for posting in posting_contents:
        try:
            posting_head = posting.find('div', attrs={'class': 'postingHead'})
            bewertung = posting_head.find('span', attrs={'class': 'likecount'}).text

            meta = posting_head.find('div', attrs={'class': 'meta'})
            zeitpunkt = meta.find("div", attrs={'class': 'timestamp'}).text
            zeitpunkt = re.sub(r" schrieb am ", "", zeitpunkt)

            benutzer = meta.find('button').text
            benutzer = benutzer.strip()

            posting_text = posting.find("div", attrs={'class': 'postingText'}).text
            posting_text = posting_text.lstrip()

            data_list.append({
                'Bewertung': bewertung,
                'Zeitpunkt': zeitpunkt,
                'Benutzer': benutzer,
                'Text': posting_text,
                'Article_URL': needed_link
            })
        except AttributeError:
            pass
    print(m)
    m = m + 1
df = pd.DataFrame(data_list)
df.to_csv('forum_content_13.csv', index=False, header=True, encoding='utf-8')