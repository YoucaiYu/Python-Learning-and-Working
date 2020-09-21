import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

article_infor = pd.read_csv('thisArticle.csv')

headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

i = 9500
new_article = []
main_url = 'https://www.wallstreet-online.de'
for link in article_infor['articleURL'][9500:]:
    complete_link = urljoin(main_url, link)
    page = requests.get(complete_link, headers=headers).content
    soup = BeautifulSoup(page, 'html.parser')
    sub_line = soup.find('div', attrs={'id':'newsArticleIdentity'})
    sub_time = sub_line.find('meta', attrs={'itemprop': 'datePublished'})['content']
    new_article.append((link, sub_time))
    print(i)
    i = i + 1

df = pd.DataFrame(new_article)
df.to_csv('new_article_timestamp.csv', mode='a', index=False, header=False, encoding='utf-8')