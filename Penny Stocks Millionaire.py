from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import facebook
import requests
import json

driver = webdriver.Chrome()
driver.get('https://mbasic.facebook.com/')

account = driver.find_element_by_xpath('//*[@id="m_login_email"]').send_keys("263493940@qq.com")
time.sleep(1)
pass_wort = driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[2]/div/input').send_keys('YouCai23664!')
time.sleep(1)
log_in = driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input').click()
time.sleep(1)


data = []
group_id = '131627633535573'
token = 'EAACEdEose0cBAOghD2Y1Wo75Dwypx63FZBcgZBmnD7gcuYHslutHIBnjO6J2XMF7krQdqlzLIQCeFvycZAVce1spDihStERzxGWhYrOl4REHcyC7FCOYKQtMUtfyQtG4mtq6KTAaEgQ7C9aG5pZA8Dem3mrBo1W8ONyU5mGP6SJhNg0MMosO5jkbBCKDScewxVp1zephFQZDZD'
main_link = 'https://graph.facebook.com/v3.0/'
share_search = '?fields=shares&access_token='
like_search = '?fields=likes&access_token='

driver.get('https://mbasic.facebook.com/groups/131627633535573?refid=46&__xts__%5B0%5D=12.%7B%22unit_id_click_type%22%3A%22graph_search_results_item_tapped%22%2C%22click_type%22%3A%22result%22%2C%22module_id%22%3A1%2C%22result_id%22%3A131627633535573%2C%22session_id%22%3A%22b68316ed51911be17f3b04ed20400774%22%2C%22module_role%22%3A%22ENTITY_GROUPS%22%2C%22unit_id%22%3A%22browse_rl%3A5ec25833-9b39-660d-e631-138eab2aef62%22%2C%22browse_result_type%22%3A%22browse_type_group%22%2C%22unit_id_result_id%22%3A131627633535573%2C%22module_result_position%22%3A0%7D')
post_page = driver.page_source

i = 0
while i < 2:
    post_page = driver.page_source
    soup = BeautifulSoup(post_page, 'html.parser')

    posts = soup.find_all('div', attrs={'class': "bu bv bw"})

    for single_post in posts:
        try:
            post_link = single_post.find('a')
            link_link = post_link.get('href')
            post_id = re.search(r'top_level_post_id\.\d+', link_link)
            post_id = str(post_id.group())
            post_id = re.sub(r'\D', "", post_id)
            new_post_id = group_id + "_" + post_id
        except AttributeError:
            continue

        graph = facebook.GraphAPI(access_token=token)
        all_posts = graph.get_object(new_post_id)

        if 'message' in all_posts:

            post_time = all_posts['created_time']
            post_content = all_posts['message']

            try:
                share_search_link = main_link + new_post_id + share_search + token
                response_share = requests.get(share_search_link)
                html_share = json.loads(response_share.text)
                count_share = html_share['shares']['count']
                like_search_link = main_link + new_post_id + like_search + token
                response_like = requests.get(like_search_link)
                html_like = json.loads(response_like.text)
                count_like = html_like['likes']['count']
            except KeyError:
                count_share = 'NA'
                count_like = 'NA'

        else:
            continue

        data.append([new_post_id, post_content, count_like, count_share, group_id, post_time])
        information_list = pd.DataFrame(data)

    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(1)

    more_load = driver.find_element_by_xpath('//*[@id="m_group_stories_container"]/div[2]/a')
    more_load.click()
    i = i + 1

information_list.to_csv('Stock Analysts_Posts.csv', index=False, header=False, encoding='utf-8')

driver.quit()