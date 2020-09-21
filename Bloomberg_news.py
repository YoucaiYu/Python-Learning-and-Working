from selenium import webdriver
import pandas as pd

from bs4 import BeautifulSoup

df = pd.read_csv('energy_bloomberg.csv', encoding='utf8')
links_list = df['Link']

news_links = ["https://www.bloomberg.com/topics/energy-industry", "https://www.bloomberg.com/topics/information-technology",
             "https://www.bloomberg.com/topics/telecommunication-services", "https://www.bloomberg.com/topics/health-care",
             "https://www.bloomberg.com/topics/materials", "https://www.bloomberg.com/topics/consumer-staples",
             "https://www.bloomberg.com/topics/finance", "https://www.bloomberg.com/topics/utilities",
             "https://www.bloomberg.com/topics/real-estate", "https://www.bloomberg.com/topics/consumer-discretionary"]


# selenium driver open
driver = webdriver.Chrome()
driver.maximize_window()

m = 1
def get_news_content(news_link):
    driver.get(news_link)

    js = "document.getElementsByClassName(“call”).click()"
    driver.execute_script(js)
    driver.find_element_by_css_selector('body > div:nth-child(15) > div.mainContent > div > div.pdynamicbutton > a.call')
    # scroll down to load news
    driver.implicitly_wait(3)
    i = 1
    while 1 <= 50:
        js = "window.scrollBy(0,800)"
        driver.execute_script(js)
        i = i + 1

    # energy
    text_page = driver.page_source
    soup = BeautifulSoup(text_page, 'html.parser')
    text_title = soup.select('.published-at')

    time_list = []
    for time in text_title:
        article_time = time["datetime"]
        time_list.append(article_time)

    b_url = 'https://www.bloomberg.com'
    title_list = []
    link_list = []
    article_titles = soup.select('.index-page__headline-link')
    for article in article_titles:
        article_title = article.text
        article_link = article['href']
        article_link_complete = urljoin(b_url, article_link)
        title_list.append(article_title)
        link_list.append(article_link_complete)

    article_dic = {'Title': title_list, 'Link': link_list, 'Time': time_list}
    # save all relevant data of energy news
    article_detail = pd.DataFrame(article_dic)
    csv_name = str(m) + "_bloomberg.csv"
    article_detail.to_csv(csv_name, mode='a', index=False, encoding='utf-8')

for link in news_links:
    get_news_content(link)
    m = m + 1