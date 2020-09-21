from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import pandas as pd

def get_lion_titles():
    main_link_lion = 'http://www.thelion.com'
    lion_link = 'http://www.thelion.com/bin/forum.cgi?tf=penny_stocks'
    page_lion = urlopen(lion_link)

    #set a list to save data
    data_lion = []
    soup = BeautifulSoup(page_lion, 'html.parser')
    table_data = soup.find('table', attrs={'id': 'f'})

    sub_data_1 = table_data.find_all('tr', attrs={'class': 'z1'})
    for detail_data in sub_data_1:
        msg_nr = detail_data.find('td', attrs={'class': 'a8'}).text
        forum_symbol = detail_data.find('td', attrs={'class': 'b'}).text
        forum_title = detail_data.find('td', attrs={'class': 'tdwrap'})
        forum_title_new = forum_title.text
        title_link = forum_title.find('a').get('href')
        title_link_new = urljoin(main_link_lion, title_link)
        # author = detail_data.find('td')
        date_1 = detail_data.find('td', attrs={'class': 'sr'}).text
        data_lion.append((msg_nr, forum_symbol, forum_title_new, title_link_new, date_1))

    sub_data_0 = table_data.find_all('tr', attrs={'class': 'z0'})
    for detail_data in sub_data_1:
        msg_nr = detail_data.find('td', attrs={'class': 'a8'}).text
        forum_symbol = detail_data.find('td', attrs={'class': 'b'}).text
        forum_title = detail_data.find('td', attrs={'class': 'tdwrap'})
        forum_title_new = forum_title.text
        title_link = forum_title.find('a').get('href')
        title_link_new = urljoin(main_link_lion, title_link)
        # author = detail_data.find('td')
        date_2 = detail_data.find('td', attrs={'class': 'sr'}).text
        data_lion.append((msg_nr, forum_symbol, forum_title_new, title_link_new, date_2))

    title_list = pd.DataFrame(data_lion)
    title_list.to_csv('Forum_Lion_title.csv', mode='a', index=False, header=False, encoding='utf-8')