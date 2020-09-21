from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
from urllib.error import HTTPError

df = pd.read_csv('Ergaenzung_link.csv', encoding='utf8')
links_list = df['Link']

infors = []
i = 1
for link in links_list:
    url = link
    try:
        page = urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')

        try:
            title_infor = soup.find('div', attrs={"class": "lede-text-v2__content"})
            tt = title_infor.find('h1').text
            t_tag = title_infor.find('div', attrs={"class": 'eyebrow-v2'}).text

            try:
                autor = title_infor.find('a').text
            # for just addressed article
            except AttributeError:
                autor = title_infor.find('address').text

            t_time = title_infor.find('time')["datetime"]
            content_box = soup.find('div', attrs={'class': 'body-copy-v2 fence-body'})
            article_contents = content_box.find_all('p')

            content = ""
            for article_content in article_contents:
                content = content + article_content.text
        except AttributeError:
            pass
        try:

            infors.append((tt, t_tag, autor, t_time, content))
            time.sleep(1)
        except NameError:
            pass

    except HTTPError:
        print("Error: ", url)
        continue
    print(i)
    i = i + 1

article_content = pd.DataFrame(infors)
# headers = ['Title', 'Tag', 'Author', 'Time', 'content']
article_content.to_csv('Test_Ergaenzung_content.csv', mode='a', index=False, header=False, encoding='utf-8')