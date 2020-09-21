from bs4 import BeautifulSoup
from urllib.request import urljoin
import pandas as pd
import requests
import re

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

initial_url = 'https://www.wallstreet-online.de/community/letzte-antworten.html?cat=4'
forum_main_page = requests.get(initial_url, headers=headers).content

soup = BeautifulSoup(forum_main_page, 'html.parser')

article_links = soup.find_all('div', attrs={'class':'bold'})

# get all article link and save them in a list
forumArticles = []
for article in article_links:
    link = article.a['href']
    forumArticles.append(link)

main_url = 'https://www.wallstreet-online.de'

complete_link_list = []
n = 1

for article_link in forumArticles:

    # combine the main link and the article link
    article_url = urljoin(main_url, article_link)
    # get the article page
    article_page = requests.get(article_url, headers=headers).content
    page_soup = BeautifulSoup(article_page, 'html.parser')
    try:
        # get the pagination
        pagination = page_soup.select('.threadPagination a')
        pagi_list = []

        for pagi in pagination:
            pagi_list.append(pagi['href'])

        pagesURL = re.sub(r"https://www.wallstreet-online.de/diskussion/", "", article_url)
        pagesURL = re.sub(r"\/", "&&", pagesURL)
        pagesURL = re.sub(r"&&[a-z0-9A-Z-]*", "", pagesURL)

        page_ID = re.sub(r"-1-10", "", pagesURL)

        pagesend = pagi_list[len(pagi_list) - 1]
        pagesURLend = re.sub(r"/diskussion/", "", pagesend)
        pagesURLend = re.sub(r"\/", "&&", pagesURLend)
        pagesURLend = re.sub(r"&&[a-z0-9A-Z-]*", "", pagesURLend)
        to_sub = page_ID + "-"
        pagesURLend = re.sub(to_sub, "", pagesURLend)
        pagesURLendpoint = re.sub(r"[0-9]*[-]", "", pagesURLend)

        page_start = list(range(1, int(pagesURLendpoint) + 1, 10))
        page_end = list(range(10, int(pagesURLendpoint) + 1, 10))
        new_list = []
        i = 0
        while i < len(page_start):
            new_aa = page_ID + "-" + str(page_start[i]) + "-" + str(page_end[i])
            i = i + 1
            new_list.append(new_aa)

        new_sub = re.sub(r"/diskussion/", "", article_link)
        new_sub = re.split(r"\/", new_sub)
        for new_url in new_list:
            complete_link = main_url + "/diskussion/" + new_url + "/" + new_sub[1]
            complete_link_list.append(complete_link)
    except IndexError:
        complete_link = article_url
        complete_link_list.append(complete_link)
    print(n)
    n = n + 1

df = pd.DataFrame(complete_link_list)
df.to_csv('Wallstreet_link.csv', index=False, header=False, encoding='utf-8')